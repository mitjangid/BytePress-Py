from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserRole


# ─────────────────────────────────────────────
# User Profile Inline (attached to User admin)
# ─────────────────────────────────────────────
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('🔧 Profile Preferences & Language')
    fk_name = 'user'
    fieldsets = (
        ('🌍 Language & Location', {
            'fields': ('preferred_language', 'preferred_location'),
            'description': 'Persistent reader language preference set on frontend (en, hi, mr, etc.) and local news location.'
        }),
        ('📧 Notifications', {
            'fields': ('email_notifications', 'newsletter_opt_in', 'dark_mode_preference'),
        }),
    )


# ─────────────────────────────────────────────
# User Admin
# ─────────────────────────────────────────────
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'full_name', 'role_badge', 'is_verified_author', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified_author', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    list_per_page = 30
    actions = ['verify_authors', 'unverify_authors', 'promote_to_editor', 'promote_to_moderator']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('👤 Personal Info'), {
            'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio')
        }),
        (_('✍️ Author Details & Socials'), {
            'fields': ('is_verified_author', 'twitter_handle', 'facebook_url', 'website'),
            'classes': ('collapse',)
        }),
        (_('🔐 Role & Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('📅 Important Dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('🔐 Role Assignment'), {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'is_verified_author'),
        }),
    )

    def role_badge(self, obj):
        colors = {
            UserRole.SUPER_ADMIN: '#7C3AED',
            UserRole.ADMIN: '#DC2626',
            UserRole.EDITOR: '#D97706',
            UserRole.AUTHOR: '#2563EB',
            UserRole.MODERATOR: '#059669',
            UserRole.SUBSCRIBER: '#6B7280',
        }
        color = colors.get(obj.role, '#6B7280')
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    def full_name(self, obj):
        return obj.get_full_name() or '—'
    full_name.short_description = 'Full Name'

    @admin.action(description='✔ Verify selected users as Authors')
    def verify_authors(self, request, queryset):
        count = queryset.update(is_verified_author=True)
        self.message_user(request, f'Verified {count} author(s).')

    @admin.action(description='✘ Remove Author verification badge')
    def unverify_authors(self, request, queryset):
        count = queryset.update(is_verified_author=False)
        self.message_user(request, f'Removed verification from {count} user(s).')

    @admin.action(description='🖊 Promote selected users to Editor role')
    def promote_to_editor(self, request, queryset):
        for user in queryset:
            user.role = UserRole.EDITOR
            user.save()
        self.message_user(request, f'Promoted {queryset.count()} user(s) to Editor.')

    @admin.action(description='🛡 Promote selected users to Moderator role')
    def promote_to_moderator(self, request, queryset):
        for user in queryset:
            user.role = UserRole.MODERATOR
            user.save()
        self.message_user(request, f'Promoted {queryset.count()} user(s) to Moderator.')


# ─────────────────────────────────────────────
# User Profile Admin (standalone)
# ─────────────────────────────────────────────
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'preferred_location', 'email_notifications', 'newsletter_opt_in', 'dark_mode_preference', 'updated_at')
    list_filter = ('preferred_language', 'email_notifications', 'newsletter_opt_in', 'dark_mode_preference')
    search_fields = ('user__username', 'user__email', 'preferred_language')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    list_editable = ('email_notifications', 'newsletter_opt_in')
    list_per_page = 30

    fieldsets = (
        ('🌍 Language & Location Preferences', {
            'fields': ('user', 'preferred_language', 'preferred_location'),
            'description': (
                '"preferred_language" is set automatically when a reader switches language '
                'on the frontend (persisted via 1-year cookie + this DB field). Values: en, hi, mr, etc.'
            )
        }),
        ('📧 Notification Preferences', {
            'fields': ('email_notifications', 'newsletter_opt_in', 'dark_mode_preference')
        }),
        ('📅 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
