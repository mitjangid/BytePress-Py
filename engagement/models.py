import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class CommentStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending Moderation')
    APPROVED = 'APPROVED', _('Approved')
    FLAGGED = 'FLAGGED', _('Flagged Spam')
    REJECTED = 'REJECTED', _('Rejected')


class Comment(models.Model):
    """
    Threaded reader comments with moderation queue and anti-spam flags.
    """
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    author_name = models.CharField(_('author name'), max_length=100, blank=True)
    author_email = models.EmailField(_('author email'), blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(_('comment content'))
    status = models.CharField(_('status'), max_length=15, choices=CommentStatus.choices, default=CommentStatus.PENDING, db_index=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('User-Agent'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        author = self.user.display_name if self.user else (self.author_name or 'Anonymous')
        return f"Comment by {author} on '{self.article.title[:30]}'"

    @property
    def display_author(self):
        if self.user:
            return self.user.display_name
        return self.author_name if self.author_name else 'Anonymous Reader'


class Bookmark(models.Model):
    """
    Bookmarks / Saved Reading List for logged-in users.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
        unique_together = ('user', 'article')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.article.title}"


class NewsletterSubscriber(models.Model):
    """
    Newsletter subscriber registry with double opt-in token.
    """
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_active = models.BooleanField(_('is active'), default=True)
    token = models.UUIDField(_('unsubscribe token'), default=uuid.uuid4, editable=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Newsletter Subscriber')
        verbose_name_plural = _('Newsletter Subscribers')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class DigestStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft')
    SENDING = 'SENDING', _('Sending')
    SENT = 'SENT', _('Sent')


class NewsletterDigest(models.Model):
    """
    Scheduled newsletter dispatch records.
    """
    subject = models.CharField(_('subject line'), max_length=255)
    articles = models.ManyToManyField('articles.Article', related_name='newsletter_digests')
    status = models.CharField(_('status'), max_length=15, choices=DigestStatus.choices, default=DigestStatus.DRAFT)
    scheduled_for = models.DateTimeField(_('scheduled send time'))
    sent_at = models.DateTimeField(_('sent at'), null=True, blank=True)

    class Meta:
        verbose_name = _('Newsletter Digest')
        verbose_name_plural = _('Newsletter Digests')
        ordering = ['-scheduled_for']

    def __str__(self):
        return self.subject


class WebPushSubscription(models.Model):
    """
    Web Push notification subscription endpoint repository.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True, related_name='push_subscriptions')
    endpoint = models.URLField(_('push endpoint'), max_length=500)
    p256dh = models.CharField(_('p256dh key'), max_length=255)
    auth = models.CharField(_('auth key'), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Web Push Subscription')
        verbose_name_plural = _('Web Push Subscriptions')
