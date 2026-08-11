from celery import shared_task
from django.utils import timezone
from .models import Article, ArticleStatus

@shared_task
def publish_scheduled_articles():
    """
    Celery Beat task running periodically to publish articles whose scheduled_at time has arrived.
    """
    now = timezone.now()
    scheduled_articles = Article.objects.filter(
        scheduled_at__lte=now,
        status__in=[ArticleStatus.DRAFT, ArticleStatus.PENDING_REVIEW]
    )
    published_count = 0
    for article in scheduled_articles:
        article.status = ArticleStatus.PUBLISHED
        if not article.published_at:
            article.published_at = article.scheduled_at
        article.save()
        published_count += 1

    return f"Successfully published {published_count} scheduled articles."
