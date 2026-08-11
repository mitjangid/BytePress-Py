from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    Article, ArticleRevision, ArticleStateLog, Tag, RelatedArticleOverride, ArticleStatus, FactCheck
)

class ArticleRevisionInline(admin.TabularInline):
    model = ArticleRevision
    extra = 0
    readonly_fields = ('version_number', 'title', 'edited_by', 'created_at')
    can_delete = False

class ArticleStateLogInline(admin.TabularInline):
    model = ArticleStateLog
    extra = 0
    readonly_fields = ('from_state', 'to_state', 'changed_by', 'notes', 'created_at')
    can_delete = False

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ArticleRevisionInline, ArticleStateLogInline)
    list_display = (
        'title', 'author', 'primary_category', 'location',
        'status_badge', 'is_breaking', 'is_featured', 'views_count', 'published_at'
    )
    fieldsets = (
        (None, {'fields': ('title', 'title_hi', 'slug', 'summary', 'summary_hi', 'content', 'content_hi')}),
        ('Categorization & Taxonomy', {'fields': ('primary_category', 'secondary_categories', 'location', 'tags')}),
        ('Media', {'fields': ('main_image',)}),
        ('Authorship', {'fields': ('author', 'co_authors')}),
        ('Workflow State', {'fields': ('status', 'published_at', 'scheduled_at')}),
        ('Content Flags', {'fields': ('is_breaking', 'is_featured', 'is_trending', 'is_editors_pick')}),
        ('Metrics', {'fields': ('views_count', 'reading_time_minutes', 'created_at', 'updated_at')}),
    )
    list_filter = ('status', 'is_breaking', 'is_featured', 'is_trending', 'is_editors_pick', 'primary_category', 'location', 'published_at')
    search_fields = ('title', 'summary', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('secondary_categories', 'co_authors', 'tags')
    readonly_fields = ('views_count', 'reading_time_minutes', 'created_at', 'updated_at')

    actions = ['make_published', 'make_pending_review', 'make_archived', 'toggle_breaking_flag']

    def status_badge(self, obj):
        colors = {
            ArticleStatus.DRAFT: '#6B7280',
            ArticleStatus.PENDING_REVIEW: '#F59E0B',
            ArticleStatus.PUBLISHED: '#10B981',
            ArticleStatus.ARCHIVED: '#EF4444',
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>', color, obj.get_status_display())
    status_badge.short_description = "Status"

    @admin.action(description=_('Bulk Action: Publish selected articles'))
    def make_published(self, request, queryset):
        count = 0
        for article in queryset:
            article.status = ArticleStatus.PUBLISHED
            article.save()
            count += 1
        self.message_user(request, f"Successfully published {count} articles.")

    @admin.action(description=_('Bulk Action: Submit selected articles for Editorial Review'))
    def make_pending_review(self, request, queryset):
        updated = queryset.update(status=ArticleStatus.PENDING_REVIEW)
        self.message_user(request, f"{updated} articles submitted for review.")

    @admin.action(description=_('Bulk Action: Archive selected articles'))
    def make_archived(self, request, queryset):
        updated = queryset.update(status=ArticleStatus.ARCHIVED)
        self.message_user(request, f"{updated} articles archived.")

    @admin.action(description=_('Bulk Action: Toggle Breaking News flag'))
    def toggle_breaking_flag(self, request, queryset):
        for article in queryset:
            article.is_breaking = not article.is_breaking
            article.save()
        self.message_user(request, "Toggled Breaking News flags.")

@admin.register(ArticleRevision)
class ArticleRevisionAdmin(admin.ModelAdmin):
    list_display = ('article', 'version_number', 'edited_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'title')

@admin.register(ArticleStateLog)
class ArticleStateLogAdmin(admin.ModelAdmin):
    list_display = ('article', 'from_state', 'to_state', 'changed_by', 'created_at')
    list_filter = ('from_state', 'to_state', 'created_at')

@admin.register(FactCheck)
class FactCheckAdmin(admin.ModelAdmin):
    list_display = ('article', 'verdict', 'claim_by', 'created_at')
    list_filter = ('verdict', 'created_at')
    search_fields = ('article__title', 'claim_text', 'explanation')
