from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from articles.models import Article, ArticleStatus, Tag, RelatedArticleOverride
from taxonomy.models import Category, Location
from accounts.models import User
from engagement.models import CommentStatus, Bookmark
from seo.utils import generate_schema_json_ld
from seo.views import get_or_create_short_url
from .models import HomepageLayout, SectionType

def homepage_view(request):
    """
    Dynamic homepage driven by database-defined HomepageLayout blocks.
    """
    layout_blocks = HomepageLayout.objects.filter(is_active=True).order_by('display_order')
    
    # Base query for published articles
    published_articles = Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related(
        'primary_category', 'location', 'author', 'main_image'
    )

    # Hero articles (top 5 published articles or breaking/featured)
    hero_articles = published_articles.filter(Q(is_featured=True) | Q(is_breaking=True)).order_by('-published_at')[:5]
    if not hero_articles.exists():
        hero_articles = published_articles.order_by('-published_at')[:5]

    hero_main = hero_articles[0] if hero_articles else None
    hero_secondary = hero_articles[1:5] if len(hero_articles) > 1 else []

    # Trending articles
    trending_articles = published_articles.order_by('-views_count', '-published_at')[:6]

    # Editor's picks
    editors_picks = published_articles.filter(is_editors_pick=True).order_by('-published_at')[:4]

    # Render blocks dynamically
    block_data = []
    for block in layout_blocks:
        qs = published_articles
        if block.category:
            qs = qs.filter(Q(primary_category=block.category) | Q(secondary_categories=block.category)).distinct()
        if block.location:
            qs = qs.filter(location=block.location)
        
        items = qs.order_by('-published_at')[:block.item_limit]
        block_data.append({
            'block': block,
            'items': items
        })

    context = {
        'hero_main': hero_main,
        'hero_secondary': hero_secondary,
        'trending_articles': trending_articles,
        'editors_picks': editors_picks,
        'block_data': block_data,
    }
    return render(request, 'core/homepage.html', context)


def article_detail_view(request, slug):
    """
    Rich article detail page with JSON-LD, author card, co-authors, tags, related stories, and HTMX comments.
    """
    article = get_object_or_404(
        Article.objects.select_related('primary_category', 'location', 'author', 'main_image')
                       .prefetch_related('co_authors', 'tags', 'secondary_categories'),
        slug=slug
    )

    # Increment view count
    Article.objects.filter(pk=article.pk).update(views_count=F('views_count') + 1)

    # Approved comments
    comments = article.comments.filter(status=CommentStatus.APPROVED, parent__isnull=True).prefetch_related('replies')

    # Manual related articles or fallback auto-suggested (same category / shared tags)
    manual_overrides = RelatedArticleOverride.objects.filter(source_article=article).select_related('target_article')
    if manual_overrides.exists():
        related_articles = [override.target_article for override in manual_overrides]
    else:
        related_articles = Article.objects.filter(
            status=ArticleStatus.PUBLISHED,
            primary_category=article.primary_category
        ).exclude(pk=article.pk).order_by('-published_at')[:4]

    # Bookmark state for current logged in user
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, article=article).exists()

    schema_json_ld = generate_schema_json_ld(article, request)
    short_url = get_or_create_short_url(request, article.get_absolute_url())

    context = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'is_bookmarked': is_bookmarked,
        'schema_json_ld': schema_json_ld,
        'short_url': short_url,
    }
    return render(request, 'core/article_detail.html', context)


def category_detail_view(request, slug):
    """
    Category landing page with subcategory filters & paginated articles.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    subcategories = category.get_children().filter(is_active=True)

    articles_qs = Article.objects.filter(
        Q(primary_category=category) | Q(secondary_categories=category),
        status=ArticleStatus.PUBLISHED
    ).distinct().select_related('author', 'main_image', 'primary_category').order_by('-published_at')

    paginator = Paginator(articles_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'subcategories': subcategories,
        'page_obj': page_obj,
    }
    return render(request, 'core/category_detail.html', context)


def location_detail_view(request, slug):
    """
    State or City location news landing page.
    """
    location = get_object_or_404(Location, slug=slug, is_active=True)
    
    # Include child cities if this location is a State
    locations_included = location.get_descendants(include_self=True)

    articles_qs = Article.objects.filter(
        location__in=locations_included,
        status=ArticleStatus.PUBLISHED
    ).select_related('author', 'main_image', 'primary_category', 'location').order_by('-published_at')

    paginator = Paginator(articles_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'location': location,
        'page_obj': page_obj,
    }
    return render(request, 'core/location_detail.html', context)


def search_view(request):
    """
    Full-text search view with category, location, and date filtering.
    """
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    location_id = request.GET.get('location')

    articles_qs = Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related(
        'primary_category', 'location', 'author', 'main_image'
    )

    if query:
        # Full text search or fallback icontains lookup
        articles_qs = articles_qs.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
        )

    if category_id:
        articles_qs = articles_qs.filter(primary_category_id=category_id)

    if location_id:
        articles_qs = articles_qs.filter(location_id=location_id)

    paginator = Paginator(articles_qs.order_by('-published_at'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'core/search_results.html', context)


def author_detail_view(request, username):
    """
    Author bio card & published articles list.
    """
    author = get_object_or_404(User, username=username)
    articles_qs = Article.objects.filter(
        Q(author=author) | Q(co_authors=author),
        status=ArticleStatus.PUBLISHED
    ).distinct().select_related('primary_category', 'main_image').order_by('-published_at')

    paginator = Paginator(articles_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'core/author_detail.html', context)


def live_tv_view(request):
    """
    Live TV streaming page with embedded widget, breaking ticker, and trending stories.
    """
    stream_url = "https://www.indiatv.in/widgets/playerlivetv?accountId=63bd2161756d5f000872bc0b&videoId=e007cf4386639_live&playerDivId=vidgyor&pip=0&piv=0&aspectRatio=16:9"
    trending_articles = Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related('primary_category', 'main_image').order_by('-views_count', '-published_at')[:6]
    context = {
        'stream_url': stream_url,
        'trending_articles': trending_articles,
    }
    return render(request, 'core/live_tv.html', context)


def shorts_view(request):
    """
    Vertical 9:16 mobile news shorts feed.
    """
    shorts_articles = Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related('primary_category', 'main_image', 'author').order_by('-published_at')[:10]
    context = {
        'articles': shorts_articles,
    }
    return render(request, 'core/shorts.html', context)

