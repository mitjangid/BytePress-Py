from django.db import models
from django.utils.translation import gettext_lazy as _

class RedirectType(models.IntegerChoices):
    PERMANENT = 301, _('301 Permanent Redirect')
    TEMPORARY = 302, _('302 Temporary Redirect')

class Redirect(models.Model):
    """
    Automatic 301/302 Redirect Manager tracking URL slug changes and preventing 404 broken links.
    """
    old_path = models.CharField(_('old URL path'), max_length=255, unique=True, db_index=True, help_text=_("e.g. '/news/old-article-slug/'"))
    new_path = models.CharField(_('new URL path'), max_length=255, help_text=_("e.g. '/news/new-article-slug/'"))
    redirect_type = models.IntegerField(_('redirect HTTP status'), choices=RedirectType.choices, default=RedirectType.PERMANENT)
    created_at = models.DateTimeField(auto_now_add=True)
    hits_count = models.PositiveIntegerField(_('redirect hits count'), default=0)

    class Meta:
        verbose_name = _('301 Redirect')
        verbose_name_plural = _('301 Redirects')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.old_path} -> {self.new_path} ({self.redirect_type})"


class SEOOverride(models.Model):
    """
    Custom per-page SEO & Social Graph Meta Tags override.
    """
    canonical_url = models.URLField(_('canonical URL'), blank=True)
    og_title = models.CharField(_('OpenGraph title'), max_length=255, blank=True)
    og_description = models.TextField(_('OpenGraph description'), blank=True)
    og_image = models.URLField(_('OpenGraph image URL'), blank=True)
    no_index = models.BooleanField(_('noindex robots tag'), default=False)
    schema_type = models.CharField(_('Schema.org type'), max_length=50, default='NewsArticle')

    class Meta:
        verbose_name = _('SEO Meta Override')
        verbose_name_plural = _('SEO Meta Overrides')

    def __str__(self):
        return f"SEO Override ({self.schema_type})"


import random
import string

class ShortenedURL(models.Model):
    """
    Internal URL Shortener service model generating compact shareable links (e.g., /s/xK9a2b/).
    """
    short_code = models.CharField(_('short code'), max_length=12, unique=True, db_index=True)
    target_url = models.CharField(_('target URL or path'), max_length=500, db_index=True)
    click_count = models.PositiveIntegerField(_('clicks count'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Shortened URL')
        verbose_name_plural = _('Shortened URLs')
        ordering = ['-created_at']

    def __str__(self):
        return f"/s/{self.short_code}/ -> {self.target_url}"

    @classmethod
    def generate_code(cls, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if not cls.objects.filter(short_code=code).exists():
                return code
