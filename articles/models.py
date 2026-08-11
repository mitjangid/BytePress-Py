import math
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.profanity import contains_profanity

class Tag(models.Model):
    name = models.CharField(_('tag name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), max_length=60, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return f"#{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArticleStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft')
    PENDING_REVIEW = 'PENDING_REVIEW', _('Pending Review')
    PUBLISHED = 'PUBLISHED', _('Published')
    ARCHIVED = 'ARCHIVED', _('Archived')


class Article(models.Model):
    """
    Core Article model with workflow state machine, revision tracking,
    alt-text mandatory validation on publish, and content flags.
    """
    title = models.CharField(_('title'), max_length=255)
    title_hi = models.CharField(_('Hindi / Regional Title'), max_length=255, blank=True, help_text=_('Hindi translation of article title.'))
    slug = models.SlugField(_('slug'), max_length=255, unique=True, db_index=True)
    summary = models.TextField(_('summary / dek'), max_length=500, help_text=_('Short deck summary used on cards & meta description fallback.'))
    summary_hi = models.TextField(_('Hindi / Regional Summary'), max_length=500, blank=True)
    content = models.TextField(_('article content'), help_text=_('Rich text body content.'))
    content_hi = models.TextField(_('Hindi / Regional Article Content'), blank=True)
    
    # Categorization & Taxonomy
    primary_category = models.ForeignKey(
        'taxonomy.Category',
        on_delete=models.PROTECT,
        related_name='primary_articles',
        verbose_name=_('primary category')
    )
    secondary_categories = models.ManyToManyField(
        'taxonomy.Category',
        blank=True,
        related_name='secondary_articles',
        verbose_name=_('secondary categories')
    )
    location = models.ForeignKey(
        'taxonomy.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name=_('news location')
    )
    
    # Media
    main_image = models.ForeignKey(
        'media_lib.MediaAsset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_articles',
        verbose_name=_('main featured image')
    )
    
    # Workflow State & Scheduling
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT,
        db_index=True
    )
    published_at = models.DateTimeField(_('published at'), null=True, blank=True, db_index=True)
    scheduled_at = models.DateTimeField(
        _('scheduled publishing time'),
        null=True,
        blank=True,
        help_text=_('Timestamp for automated scheduled publishing via Celery Beat.')
    )

    # Content Flags
    is_breaking = models.BooleanField(_('is breaking news'), default=False, db_index=True)
    is_featured = models.BooleanField(_('is featured story'), default=False, db_index=True)
    is_trending = models.BooleanField(_('is trending story'), default=False, db_index=True)
    is_editors_pick = models.BooleanField(_("is editor's pick"), default=False, db_index=True)

    # Authorship & Tags
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='authored_articles',
        verbose_name=_('primary author')
    )
    co_authors = models.ManyToManyField(
        'accounts.User',
        blank=True,
        related_name='co_authored_articles',
        verbose_name=_('co-authors')
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name=_('tags'))

    # Metrics
    views_count = models.PositiveIntegerField(_('views count'), default=0)
    reading_time_minutes = models.PositiveIntegerField(_('reading time (minutes)'), default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-published_at', '-created_at']
        permissions = [
            ('can_publish_article', 'Can approve and publish articles'),
            ('can_manage_featured', 'Can flag breaking and featured news'),
        ]

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'slug': self.slug})

    def get_display_title(self, lang_code='en'):
        if lang_code.startswith('hi') and self.title_hi:
            return self.title_hi
        return self.title

    def get_display_summary(self, lang_code='en'):
        if lang_code.startswith('hi') and self.summary_hi:
            return self.summary_hi
        return self.summary

    def get_display_content(self, lang_code='en'):
        if lang_code.startswith('hi') and self.content_hi:
            return self.content_hi
        return self.content

    def clean(self):
        """Validate alt-text on publish AND check for foul language in all text fields."""
        super().clean()

        # --- Profanity check on all text fields ---
        text_fields = {
            'title': self.title or '',
            'summary': self.summary or '',
            'content': self.content or '',
            'title_hi': self.title_hi or '',
            'summary_hi': self.summary_hi or '',
        }
        errors = {}
        for field_name, value in text_fields.items():
            found, words = contains_profanity(value)
            if found:
                errors[field_name] = ValidationError(
                    _(f"This field contains inappropriate language. Please revise before saving.")
                )
        if errors:
            raise ValidationError(errors)

        # --- Alt-text enforcement on publish ---
        if self.status == ArticleStatus.PUBLISHED:
            if self.main_image and not self.main_image.alt_text.strip():
                raise ValidationError({
                    'main_image': _("Cannot publish article: Main featured image must have verified Alt-Text for accessibility & SEO.")
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Calculate estimated reading time (approx 200 words per minute)
        word_count = len(self.content.split()) if self.content else 0
        self.reading_time_minutes = max(1, math.ceil(word_count / 200))

        # Auto-set published_at when state becomes PUBLISHED if not already set
        if self.status == ArticleStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Create Article Revision snapshot
        latest_rev = self.revisions.order_by('-version_number').first()
        next_version = (latest_rev.version_number + 1) if latest_rev else 1

        ArticleRevision.objects.create(
            article=self,
            version_number=next_version,
            title=self.title,
            summary=self.summary,
            content=self.content,
            edited_by=self.author
        )


class ArticleRevision(models.Model):
    """
    Article Revision snapshot model preserving full revision history and rollback capabilities.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='revisions')
    version_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    edited_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Article Revision')
        verbose_name_plural = _('Article Revisions')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.article.title} - v{self.version_number}"


class ArticleStateLog(models.Model):
    """
    Audit log tracking all workflow state transitions (Draft -> Review -> Published).
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='state_logs')
    from_state = models.CharField(max_length=20, choices=ArticleStatus.choices)
    to_state = models.CharField(max_length=20, choices=ArticleStatus.choices)
    changed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Article State Log')
        verbose_name_plural = _('Article State Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.article.title}: {self.from_state} -> {self.to_state}"


class RelatedArticleOverride(models.Model):
    """
    Manual editor override for suggested related articles.
    """
    source_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='manual_related_sources')
    target_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='manual_related_targets')
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Related Article Override')
        verbose_name_plural = _('Related Article Overrides')
        ordering = ['position']
        unique_together = ('source_article', 'target_article')


class FactCheckVerdict(models.TextChoices):
    TRUE = 'TRUE', _('सत्य / True')
    FALSE = 'FALSE', _('असत्य / False')
    MISLEADING = 'MISLEADING', _('भ्रामक / Misleading')


class FactCheck(models.Model):
    """
    Fact Check verification rating model for combating viral fake news.
    """
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='fact_check')
    claim_text = models.CharField(_('claim text'), max_length=255, help_text=_('Viral statement or post being verified.'))
    claim_by = models.CharField(_('claimed by'), max_length=150, default=_('Social Media / Viral Forward'))
    verdict = models.CharField(_('verdict'), max_length=20, choices=FactCheckVerdict.choices, default=FactCheckVerdict.FALSE)
    explanation = models.TextField(_('fact check explanation'), help_text=_('Detailed reasoning behind the rating verdict.'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Fact Check Verification')
        verbose_name_plural = _('Fact Check Verifications')

    def __str__(self):
        return f"Fact Check [{self.get_verdict_display()}]: {self.claim_text[:40]}"
