from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Comment, Bookmark, NewsletterSubscriber, NewsletterDigest, WebPushSubscription, CommentStatus


# ─────────────────────────────────────────────
# Comment Moderation Admin
# ─────────────────────────────────────────────
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_author', 'article_link', 'content_snippet', 'status_badge', 'ip_address', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('content', 'author_name', 'author_email', 'user__username', 'article__title')
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'user')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = ['approve_comments', 'mark_as_spam', 'reject_comments']
    list_per_page = 30

    fieldsets = (
        ('💬 Comment', {
            'fields': ('article', 'parent', 'content', 'status')
        }),
        ('👤 Author', {
            'fields': ('user', 'author_name', 'author_email')
        }),
        ('🔍 Meta', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            CommentStatus.APPROVED: ('#10B981', '✔ Approved'),
            CommentStatus.PENDING: ('#F59E0B', '⏳ Pending'),
            CommentStatus.FLAGGED: ('#EF4444', '🚩 Flagged'),
            CommentStatus.REJECTED: ('#6B7280', '✘ Rejected'),
        }
        color, label = colors.get(obj.status, ('#6B7280', obj.get_status_display()))
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Status'

    def content_snippet(self, obj):
        text = obj.content[:80] + '…' if len(obj.content) > 80 else obj.content
        return format_html('<span style="color:#374151;">{}</span>', text)
    content_snippet.short_description = 'Comment'

    def article_link(self, obj):
        return format_html(
            '<a href="/article/{}/" target="_blank" style="color:#d81b60; font-size:12px;">{}</a>',
            obj.article.slug, obj.article.title[:40]
        )
    article_link.short_description = 'Article'

    @admin.action(description='✔ Approve selected comments')
    def approve_comments(self, request, queryset):
        count = queryset.update(status=CommentStatus.APPROVED)
        self.message_user(request, f'✔ Approved {count} comment(s).')

    @admin.action(description='🚩 Flag selected comments as Spam')
    def mark_as_spam(self, request, queryset):
        count = queryset.update(status=CommentStatus.FLAGGED)
        self.message_user(request, f'🚩 Flagged {count} comment(s) as spam.')

    @admin.action(description='✘ Reject selected comments')
    def reject_comments(self, request, queryset):
        count = queryset.update(status=CommentStatus.REJECTED)
        self.message_user(request, f'✘ Rejected {count} comment(s).')


# ─────────────────────────────────────────────
# Bookmarks Admin
# ─────────────────────────────────────────────
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article_link', 'created_at')
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def article_link(self, obj):
        return format_html('<a href="/article/{}/" target="_blank">{}</a>', obj.article.slug, obj.article.title[:50])
    article_link.short_description = 'Article'


# ─────────────────────────────────────────────
# Newsletter Subscribers Admin
# ─────────────────────────────────────────────
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'status_badge', 'subscribed_at', 'token')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('token', 'subscribed_at')
    ordering = ('-subscribed_at',)
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']
    list_per_page = 50

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#10B981; font-weight:bold;">✔ Active</span>')
        return format_html('<span style="color:#EF4444; font-weight:bold;">✘ Unsubscribed</span>')
    status_badge.short_description = 'Status'

    @admin.action(description='✔ Activate selected subscribers')
    def activate_subscribers(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'Activated {count} subscriber(s).')

    @admin.action(description='✘ Unsubscribe selected subscribers')
    def deactivate_subscribers(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'Unsubscribed {count} subscriber(s).')


# ─────────────────────────────────────────────
# Newsletter Digest Admin
# ─────────────────────────────────────────────
@admin.register(NewsletterDigest)
class NewsletterDigestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status_badge', 'scheduled_for', 'sent_at', 'article_count')
    list_filter = ('status', 'scheduled_for')
    search_fields = ('subject',)
    readonly_fields = ('sent_at',)
    filter_horizontal = ('articles',)

    def status_badge(self, obj):
        colors = {
            'DRAFT': ('#6B7280', '📝 Draft'),
            'SENDING': ('#F59E0B', '📤 Sending'),
            'SENT': ('#10B981', '✔ Sent'),
        }
        color, label = colors.get(obj.status, ('#6B7280', obj.status))
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Status'

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = '# Articles'


# ─────────────────────────────────────────────
# Web Push Subscriptions Admin
# ─────────────────────────────────────────────
@admin.register(WebPushSubscription)
class WebPushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint_short', 'created_at')
    readonly_fields = ('endpoint', 'p256dh', 'auth', 'created_at')
    search_fields = ('user__username',)

    def endpoint_short(self, obj):
        return obj.endpoint[:60] + '…' if len(obj.endpoint) > 60 else obj.endpoint
    endpoint_short.short_description = 'Push Endpoint'
