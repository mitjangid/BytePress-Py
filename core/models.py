from django.db import models
from django.utils.translation import gettext_lazy as _

class SectionType(models.TextChoices):
    HERO = 'HERO', _('Hero Main Banner & Grid')
    TICKER = 'TICKER', _('Breaking News Ticker')
    FEATURED_GRID = 'FEATURED_GRID', _('Featured Stories Grid')
    CATEGORY_ROW = 'CATEGORY_ROW', _('Category Content Row')
    LOCATION_ROW = 'LOCATION_ROW', _('Local News Row (State/City)')
    TRENDING_LIST = 'TRENDING_LIST', _('Trending Most Read Sidebar')
    EDITOR_PICK = 'EDITOR_PICK', _("Editor's Picks Showcase")


class HomepageLayout(models.Model):
    """
    Database-driven dynamic layout engine allowing admins to rearrange content blocks on the homepage.
    """
    title = models.CharField(_('section title'), max_length=100)
    section_type = models.CharField(_('section layout type'), max_length=20, choices=SectionType.choices, default=SectionType.HERO)
    category = models.ForeignKey('taxonomy.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('filter category'))
    location = models.ForeignKey('taxonomy.Location', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('filter location'))
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True, db_index=True)
    item_limit = models.PositiveIntegerField(_('items count limit'), default=5)

    class Meta:
        verbose_name = _('Homepage Layout Block')
        verbose_name_plural = _('Homepage Layout Blocks')
        ordering = ['display_order']

    def __str__(self):
        return f"{self.display_order}. {self.title} ({self.get_section_type_display()})"


class SiteSetting(models.Model):
    """
    Singleton Site Settings model for logo, theme colors, contact info, and social links.
    """
    site_name = models.CharField(_('site name'), max_length=100, default='Headlines')
    logo = models.ImageField(_('site logo'), upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(_('site favicon'), upload_to='settings/', blank=True, null=True)
    primary_color = models.CharField(_('primary theme color'), max_length=20, default='#1E3A8A')
    secondary_color = models.CharField(_('secondary accent color'), max_length=20, default='#D97706')
    footer_text = models.TextField(_('footer copyright text'), default='© Headlines CMS. All rights reserved.')
    contact_email = models.EmailField(_('contact email'), default='contact@headlines.example.com')
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    twitter_url = models.URLField(_('Twitter / X URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True)

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return f"Site Settings ({self.site_name})"

    def save(self, *args, **kwargs):
        """Ensure singleton pattern (only one SiteSetting instance exists)."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
