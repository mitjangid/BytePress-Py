from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum
from .models import HomepageLayout, SiteSetting
from .filter_models import BlockedWord, ProfanityLog


# ─────────────────────────────────────────────
# Homepage Layout Admin
# ─────────────────────────────────────────────
@admin.register(HomepageLayout)
class HomepageLayoutAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'title', 'section_type', 'category', 'location', 'item_limit', 'is_active')
    list_display_links = ('title',)
    list_editable = ('display_order', 'is_active', 'item_limit')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title',)
    ordering = ('display_order',)


# ─────────────────────────────────────────────
# Site Settings Admin
# ─────────────────────────────────────────────
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'primary_color', 'secondary_color')
    fieldsets = (
        ('🏷️ Branding', {
            'fields': ('site_name', 'logo', 'favicon', 'footer_text')
        }),
        ('🎨 Theme Colors', {
            'fields': ('primary_color', 'secondary_color'),
            'description': 'Hex color codes for the site theme (e.g. #d81b60).'
        }),
        ('📬 Contact', {
            'fields': ('contact_email',)
        }),
        ('🔗 Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────
# Profanity Filter — Blocked Words Admin
# ─────────────────────────────────────────────
@admin.register(BlockedWord)
class BlockedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'language', 'is_active', 'is_active_badge', 'added_by', 'created_at')
    list_display_links = ('word',)
    list_filter = ('language', 'is_active', 'created_at')
    search_fields = ('word',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    ordering = ('word',)
    actions = ['activate_words', 'deactivate_words']

    fieldsets = (
        ('🔤 Word Details', {
            'fields': ('word', 'language', 'is_active'),
            'description': (
                'Words are matched case-insensitively and detect common obfuscations '
                '(e.g. "@ss" for "ass", "sh1t" for "shit"). '
                'These extend the built-in static word list.'
            )
        }),
        ('📋 Meta', {
            'fields': ('added_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #10B981; font-weight: bold;">✔ Active</span>')
        return format_html('<span style="color: #9CA3AF;">✘ Disabled</span>')
    is_active_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not obj.added_by:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='✔ Activate selected blocked words')
    def activate_words(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'Activated {count} blocked word(s).')

    @admin.action(description='✘ Deactivate selected blocked words')
    def deactivate_words(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'Deactivated {count} blocked word(s).')


# ─────────────────────────────────────────────
# Profanity Log Admin (read-only audit trail)
# ─────────────────────────────────────────────
@admin.register(ProfanityLog)
class ProfanityLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'source_badge', 'user', 'ip_address', 'matched_words', 'snippet')
    list_filter = ('source', 'created_at')
    search_fields = ('flagged_text', 'matched_words', 'user__username', 'ip_address')
    readonly_fields = ('source', 'flagged_text', 'matched_words', 'ip_address', 'user', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def source_badge(self, obj):
        colors = {
            'comment': '#F59E0B',
            'article': '#EF4444',
            'author_name': '#8B5CF6',
        }
        color = colors.get(obj.source, '#6B7280')
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, obj.get_source_display()
        )
    source_badge.short_description = 'Source'

    def snippet(self, obj):
        text = obj.flagged_text[:80] + '…' if len(obj.flagged_text) > 80 else obj.flagged_text
        return format_html('<span style="color:#EF4444; font-style:italic;">{}</span>', text)
    snippet.short_description = 'Content Snippet'
