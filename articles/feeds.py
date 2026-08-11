from django.contrib.syndication.views import Feed
from articles.models import Article, ArticleStatus

class LatestArticlesFeed(Feed):
    title = "BytePress - Latest Headlines RSS Feed"
    link = "/"
    description = "Real-time breaking headlines, national news, politics, technology, and market analysis from BytePress."

    def items(self):
        return Article.objects.filter(status=ArticleStatus.PUBLISHED).order_by('-published_at')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_pubdate(self, item):
        return item.published_at

    def item_link(self, item):
        return item.get_absolute_url()
