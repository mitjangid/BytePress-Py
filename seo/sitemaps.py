from django.contrib.sitemaps import Sitemap
from articles.models import Article, ArticleStatus
from taxonomy.models import Category, Location

class ArticleSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.9

    def items(self):
        return Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related('primary_category')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/article/{obj.slug}/"


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return f"/category/{obj.slug}/"


class LocationSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Location.objects.filter(is_active=True)

    def location(self, obj):
        return f"/location/{obj.slug}/"
