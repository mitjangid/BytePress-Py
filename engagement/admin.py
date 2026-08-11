from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Comment, Bookmark, NewsletterSubscriber, NewsletterDigest, WebPushSubscription, CommentStatus

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_author', 'article', 'status_badge', 'ip_address', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('content', 'author_name', 'author_email', 'user__username', 'article__title')
    actions = ['approve_comments', 'mark_as_spam', 'reject_comments']

    def status_badge(self, obj):
        colors = {
            CommentStatus.APPROVED: '#10B981',
            CommentStatus.PENDING: '#F59E0B',
            CommentStatus.FLAGGED: '#EF4444',
            CommentStatus.REJECTED: '#6B7280',
        }
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>', colors.get(obj.status, '#6B7280'), obj.get_status_display())
    status_badge.short_description = "Status"

    @admin.action(description=_('Moderation: Approve selected comments'))
    def approve_comments(self, request, queryset):
        count = queryset.update(status=CommentStatus.APPROVED)
        self.message_user(request, f"Approved {count} comments.")

    @admin.action(description=_('Moderation: Flag selected comments as Spam'))
    def mark_as_spam(self, request, queryset):
        count = queryset.update(status=CommentStatus.FLAGGED)
        self.message_user(request, f"Flagged {count} comments as spam.")

    @admin.action(description=_('Moderation: Reject selected comments'))
    def reject_comments(self, request, queryset):
        count = queryset.update(status=CommentStatus.REJECTED)
        self.message_user(request, f"Rejected {count} comments.")

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)

@admin.register(NewsletterDigest)
class NewsletterDigestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'scheduled_for', 'sent_at')
    list_filter = ('status', 'scheduled_for')

@admin.register(WebPushSubscription)
class WebPushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'created_at')
