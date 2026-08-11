"""
BytePress Profanity Filter Admin
Provides a database-driven custom blocked word list that extends
the hardcoded word list in core/profanity.py.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class BlockedWord(models.Model):
    """
    Admin-manageable custom blocked word/phrase list.
    Extends the built-in profanity word list in core/profanity.py.
    """
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi / Hinglish'),
        ('mr', 'Marathi'),
        ('other', 'Other / Universal'),
    ]

    word = models.CharField(
        _('word or phrase'),
        max_length=100,
        unique=True,
        help_text=_('Enter the word or phrase to block. Case-insensitive.')
    )
    language = models.CharField(
        _('language'),
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Uncheck to temporarily disable this filter.'))
    added_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blocked_words',
        verbose_name=_('added by')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Blocked Word')
        verbose_name_plural = _('Blocked Words')
        ordering = ['word']

    def __str__(self):
        return f'"{self.word}" [{self.get_language_display()}]{"" if self.is_active else " (disabled)"}'


class ProfanityLog(models.Model):
    """
    Audit log of every profanity filter trigger across the site.
    """
    SOURCE_CHOICES = [
        ('comment', 'Comment'),
        ('article', 'Article'),
        ('author_name', 'Author Name / Display Name'),
    ]

    source = models.CharField(_('source'), max_length=20, choices=SOURCE_CHOICES, db_index=True)
    flagged_text = models.TextField(_('flagged content snippet'), help_text=_('First 300 chars of the flagged text.'))
    matched_words = models.CharField(_('matched words'), max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profanity_flags',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Profanity Log')
        verbose_name_plural = _('Profanity Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_source_display()}] flagged at {self.created_at.strftime("%Y-%m-%d %H:%M")}'
