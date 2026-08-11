from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile Preferences')
    fk_name = 'user'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Customized User Admin panel with role choices, author profile fields,
    and profile preferences inline.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'role', 'is_verified_author', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_verified_author', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio')}),
        (_('Author Details & Socials'), {'fields': ('is_verified_author', 'twitter_handle', 'facebook_url', 'website')}),
        (_('Role & Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Role Assignment'), {
            'classes': ('wide',),
            'fields': ('email', 'role', 'is_verified_author'),
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'newsletter_opt_in', 'dark_mode_preference', 'created_at')
    list_filter = ('email_notifications', 'newsletter_opt_in', 'dark_mode_preference')
    search_fields = ('user__username', 'user__email')
