from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core.views import (
    homepage_view, article_detail_view, category_detail_view,
    location_detail_view, search_view, author_detail_view, live_tv_view, shorts_view
)
from engagement.views import post_comment, toggle_bookmark, subscribe_newsletter
from seo.views import robots_txt_view, redirect_short_url_view
from articles.feeds import LatestArticlesFeed
from seo.sitemaps import ArticleSitemap, CategorySitemap, LocationSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'locations': LocationSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Reader Frontend Core Views
    path('', homepage_view, name='homepage'),
    path('live-tv/', live_tv_view, name='live_tv'),
    path('shorts/', shorts_view, name='shorts'),
    path('article/<slug:slug>/', article_detail_view, name='article_detail'),
    path('category/<slug:slug>/', category_detail_view, name='category_detail'),
    path('location/<slug:slug>/', location_detail_view, name='location_detail'),
    path('author/<str:username>/', author_detail_view, name='author_detail'),
    path('search/', search_view, name='search'),

    # Interactivity & Engagement Views
    path('comment/post/<slug:article_slug>/', post_comment, name='post_comment'),
    path('bookmark/toggle/<slug:article_slug>/', toggle_bookmark, name='toggle_bookmark'),
    path('newsletter/subscribe/', subscribe_newsletter, name='subscribe_newsletter'),

    # Multilingual Language Switcher
    path('i18n/', include('django.conf.urls.i18n')),

    # SEO & Sitemaps & RSS Feeds & Internal URL Shortener
    path('s/<str:code>/', redirect_short_url_view, name='redirect_short_url'),
    path('feed/', LatestArticlesFeed(), name='rss_feed'),
    path('rss/', LatestArticlesFeed(), name='rss_feed_alt'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # REST API
    path('api/v1/', include('api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
