from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """
    Hierarchical Category model powered by django-mptt.
    Supports nested categories (e.g. World -> Europe -> UK).
    """
    name = models.CharField(_('category name'), max_length=100)
    name_hi = models.CharField(_('category name (Hindi / Regional)'), max_length=100, blank=True, help_text=_("e.g. तकनीक, राजनीति, खेल"))
    slug = models.SlugField(_('slug'), max_length=120, unique=True, db_index=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent category')
    )
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon class'), max_length=50, blank=True, help_text=_("FontAwesome or CSS icon class e.g., 'fa-globe'"))
    is_active = models.BooleanField(_('is active'), default=True, db_index=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    
    # SEO overrides
    meta_title = models.CharField(_('meta title'), max_length=150, blank=True, help_text=_('Custom SEO page title override.'))
    meta_description = models.TextField(_('meta description'), blank=True, help_text=_('Custom SEO meta description override.'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['display_order', 'name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['display_order', 'name']

    def __str__(self):
        ancestors = self.get_ancestors(include_self=True)
        return ' > '.join([a.name for a in ancestors])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LocationType(models.TextChoices):
    STATE = 'STATE', _('State / Region')
    CITY = 'CITY', _('City')


class Location(MPTTModel):
    """
    Two-tier geographical location model (State -> City) for localized news filtering.
    """
    name = models.CharField(_('location name'), max_length=100)
    name_hi = models.CharField(_('location name (Hindi / Regional)'), max_length=100, blank=True, help_text=_("e.g. दिल्ली, मुंबई, उत्तर प्रदेश"))
    slug = models.SlugField(_('slug'), max_length=120, unique=True, db_index=True)
    location_type = models.CharField(
        _('location type'),
        max_length=10,
        choices=LocationType.choices,
        default=LocationType.STATE
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent state / region')
    )
    state_code = models.CharField(_('state code'), max_length=10, blank=True, help_text=_("e.g. CA, NY, TX"))
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.name}, {self.parent.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
