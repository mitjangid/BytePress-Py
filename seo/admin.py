from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Redirect, SEOOverride, ShortenedURL


# ─────────────────────────────────────────────
# 301/302 Redirect Manager
# ─────────────────────────────────────────────
@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'redirect_type_badge', 'hits_count', 'created_at')
    list_filter = ('redirect_type', 'created_at')
    search_fields = ('old_path', 'new_path')
    readonly_fields = ('hits_count', 'created_at')
    ordering = ('-hits_count',)

    def redirect_type_badge(self, obj):
        color = '#10B981' if obj.redirect_type == 301 else '#F59E0B'
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, f'{obj.redirect_type} {"Permanent" if obj.redirect_type == 301 else "Temporary"}'
        )
    redirect_type_badge.short_description = 'Type'


# ─────────────────────────────────────────────
# SEO Meta Override
# ─────────────────────────────────────────────
@admin.register(SEOOverride)
class SEOOverrideAdmin(admin.ModelAdmin):
    list_display = ('canonical_url', 'og_title', 'schema_type', 'no_index_badge')
    search_fields = ('canonical_url', 'og_title')

    def no_index_badge(self, obj):
        if obj.no_index:
            return format_html('<span style="color:#EF4444; font-weight:bold;">🚫 No-Index</span>')
        return format_html('<span style="color:#10B981; font-weight:bold;">✔ Indexed</span>')
    no_index_badge.short_description = 'Robots'


# ─────────────────────────────────────────────
# Internal URL Shortener — /s/<code>/
# ─────────────────────────────────────────────
@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('short_link', 'target_url_display', 'clicks_badge', 'created_at')
    search_fields = ('short_code', 'target_url')
    readonly_fields = ('short_code', 'click_count', 'created_at', 'short_link')
    ordering = ('-click_count',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('🔗 Short Link', {
            'fields': ('short_link', 'short_code', 'target_url'),
        }),
        ('📊 Analytics', {
            'fields': ('click_count', 'created_at'),
        }),
    )

    def short_link(self, obj):
        return format_html(
            '<a href="/s/{}/" target="_blank" style="font-family:monospace; color:#d81b60; font-weight:bold;">/s/{}/</a>',
            obj.short_code, obj.short_code
        )
    short_link.short_description = 'Short URL'

    def target_url_display(self, obj):
        label = obj.target_url[:60] + '…' if len(obj.target_url) > 60 else obj.target_url
        return format_html('<a href="{}" target="_blank">{}</a>', obj.target_url, label)
    target_url_display.short_description = 'Target URL'

    def clicks_badge(self, obj):
        color = '#10B981' if obj.click_count > 100 else ('#F59E0B' if obj.click_count > 10 else '#6B7280')
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-weight:bold; font-size:12px;">📈 {:,}</span>',
            color, obj.click_count
        )
    clicks_badge.short_description = 'Clicks'

    def has_add_permission(self, request):
        # Short URLs are auto-generated from article detail pages, not manually created
        return False
