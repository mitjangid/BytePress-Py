from django.http import HttpResponse

def robots_txt_view(request):
    """
    Renders dynamic robots.txt content.
    """
    domain = request.build_absolute_uri('/')[:-1]
    content = f"""User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /search/

Sitemap: {domain}/sitemap.xml
Sitemap: {domain}/sitemap-articles.xml
"""
    return HttpResponse(content, content_type="text/plain")


from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from .models import ShortenedURL

def redirect_short_url_view(request, code):
    """
    Internal URL shortener redirect view (/s/<str:code>/).
    Increments click count and performs a 301 Permanent Redirect to target URL.
    """
    short_url = get_object_or_404(ShortenedURL, short_code=code)
    ShortenedURL.objects.filter(pk=short_url.pk).update(click_count=F('click_count') + 1)
    return redirect(short_url.target_url, permanent=True)


def get_or_create_short_url(request, target_url):
    """
    Utility function returning absolute short URL for any path or URL.
    """
    short_obj, created = ShortenedURL.objects.get_or_create(
        target_url=target_url,
        defaults={'short_code': ShortenedURL.generate_code()}
    )
    return request.build_absolute_uri(f'/s/{short_obj.short_code}/')
