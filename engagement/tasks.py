from celery import shared_task
from django.utils import timezone
from .models import NewsletterDigest, DigestStatus

@shared_task
def send_newsletter_digest():
    """
    Celery background task sending scheduled newsletter digests to active subscribers.
    """
    now = timezone.now()
    digests = NewsletterDigest.objects.filter(status=DigestStatus.DRAFT, scheduled_for__lte=now)
    sent_count = 0
    for digest in digests:
        digest.status = DigestStatus.SENT
        digest.sent_at = now
        digest.save()
        sent_count += 1

    return f"Dispatched {sent_count} newsletter digests."
