from django.contrib import admin
from django.utils.html import format_html
from .models import MediaAsset, VideoEmbed

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('preview_thumbnail', 'title', 'file_type', 'alt_text_status', 'uploaded_by', 'width', 'height', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('title', 'alt_text', 'caption')
    readonly_fields = ('width', 'height', 'file_size', 'preview_thumbnail', 'created_at', 'updated_at')

    def preview_thumbnail(self, obj):
        if obj.file:
            return format_html('<img src="{}" style="height: 50px; width: auto; border-radius: 4px;" />', obj.file.url)
        return "-"
    preview_thumbnail.short_description = "Preview"

    def alt_text_status(self, obj):
        if obj.alt_text:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: red;">✗ Missing Alt-Text</span>')
    alt_text_status.short_description = "Alt-Text Status"

@admin.register(VideoEmbed)
class VideoEmbedAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'embed_id', 'uploaded_by', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('title', 'video_url', 'embed_id')
