from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
    ADMIN = 'ADMIN', _('Admin')
    EDITOR = 'EDITOR', _('Editor')
    AUTHOR = 'AUTHOR', _('Author / Reporter')
    MODERATOR = 'MODERATOR', _('Moderator')
    SUBSCRIBER = 'SUBSCRIBER', _('Subscriber / Reader')


class User(AbstractUser):
    """
    Custom User Model for Headlines CMS supporting email authentication,
    role choices, author profiles, and custom permissions.
    """
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.SUBSCRIBER,
        help_text=_('Designates the role and permission tier of the user within Headlines CMS.')
    )
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('author bio'), blank=True, help_text=_('Short biography for author bio box on articles.'))
    twitter_handle = models.CharField(_('Twitter handle'), max_length=50, blank=True)
    facebook_url = models.URLField(_('Facebook profile URL'), max_length=255, blank=True)
    website = models.URLField(_('personal website'), max_length=255, blank=True)
    is_verified_author = models.BooleanField(
        _('verified author'),
        default=False,
        help_text=_('Designates whether this author display badge is verified.')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.get_full_name()} ({self.username})"
        return self.username

    def save(self, *args, **kwargs):
        """Automatically set is_staff status based on role."""
        if self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EDITOR, UserRole.AUTHOR, UserRole.MODERATOR]:
            self.is_staff = True
        elif self.role == UserRole.SUBSCRIBER and not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.username

    @property
    def is_super_admin(self):
        return self.role == UserRole.SUPER_ADMIN or self.is_superuser

    @property
    def is_admin(self):
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN] or self.is_superuser

    @property
    def is_editor(self):
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EDITOR] or self.is_superuser

    @property
    def is_author(self):
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EDITOR, UserRole.AUTHOR] or self.is_superuser

    @property
    def is_moderator(self):
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MODERATOR] or self.is_superuser


class UserProfile(models.Model):
    """
    Extended user profile for preferences, notifications, and reader bookmarks.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_location = models.ForeignKey(
        'taxonomy.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_by_profiles',
        verbose_name=_('preferred location')
    )
    email_notifications = models.BooleanField(_('receive email notifications'), default=True)
    newsletter_opt_in = models.BooleanField(_('subscribed to newsletter'), default=True)
    dark_mode_preference = models.BooleanField(_('dark mode enabled'), default=False)
    preferred_language = models.CharField(_('preferred language'), max_length=10, default='en', help_text=_('Persistent reader language preference (e.g. en, hi, mr).'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.username}"
