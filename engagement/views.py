from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from articles.models import Article
from taxonomy.services import get_request_client_ip
from .models import Comment, Bookmark, NewsletterSubscriber, CommentStatus
from .forms import CommentForm, NewsletterForm

@require_POST
def post_comment(request, article_slug):
    """
    HTMX view handling live comment submission with basic spam heuristics
    and foul language detection via the BytePress Profanity Filter.
    Auto-approves comments from logged-in users; guest comments undergo spam checks.
    """
    article = get_object_or_404(Article, slug=article_slug)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article

        client_ip, _ = get_request_client_ip(request)
        comment.ip_address = client_ip
        comment.user_agent = request.META.get('HTTP_USER_AGENT', '')

        if request.user.is_authenticated:
            comment.user = request.user
            comment.author_name = request.user.display_name
            comment.author_email = request.user.email
            comment.status = CommentStatus.APPROVED
        else:
            # Basic anti-spam heuristic: reject if links > 2 or blank content
            link_count = comment.content.count('http://') + comment.content.count('https://')
            if link_count > 2 or len(comment.content.strip()) < 3:
                comment.status = CommentStatus.FLAGGED
            else:
                comment.status = CommentStatus.PENDING

        comment.save()

        # If HTMX request, return partial HTML snippet with success toast
        if request.headers.get('HX-Request'):
            return render(request, 'engagement/partials/comment_item.html', {
                'comment': comment,
                'show_toast': True
            })

        return redirect(f"/article/{article.slug}/#comment-{comment.id}")

    # Form is invalid — build user-friendly error message
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(error)

    error_html = " ".join(error_messages) or "Invalid comment. Please review your input."

    if request.headers.get('HX-Request'):
        return render(request, 'engagement/partials/comment_error.html', {
            'error': error_html
        }, status=400)

    return HttpResponse(error_html, status=400)


@require_POST
def toggle_bookmark(request, article_slug):
    """
    Toggles bookmark status for an article.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to save bookmarks.'}, status=401)

    article = get_object_or_404(Article, slug=article_slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)

    if not created:
        bookmark.delete()
        is_bookmarked = False
    else:
        is_bookmarked = True

    if request.headers.get('HX-Request'):
        return render(request, 'engagement/partials/bookmark_button.html', {
            'article': article,
            'is_bookmarked': is_bookmarked
        })

    return JsonResponse({'status': 'success', 'is_bookmarked': is_bookmarked})


from django.core.mail import send_mail

@require_POST
def subscribe_newsletter(request):
    """
    Newsletter opt-in view.
    """
    email = request.POST.get('email', '').strip()
    if email:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()

        # Send Welcome Confirmation Email
        try:
            send_mail(
                subject="Welcome to Indian News Daily Newsletter! 🗞️",
                message="Thank you for subscribing to Indian News! You will receive our top daily headlines every morning.",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=True
            )
        except Exception:
            pass

        if request.headers.get('HX-Request'):
            return render(request, 'engagement/partials/newsletter_success.html', {'email': email})
        return redirect('/')

    return HttpResponse("Please provide a valid email", status=400)
