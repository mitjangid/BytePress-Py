import os
import re
from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

class MediaType(models.TextChoices):
    IMAGE = 'IMAGE', _('Image')
    VIDEO = 'VIDEO', _('Video')

class MediaAsset(models.Model):
    """
    Central Media Asset library handling auto-resizing, Pillow WebP conversion,
    metadata tracking, and required alt-text enforcement.
    """
    title = models.CharField(_('asset title'), max_length=255)
    file = models.ImageField(_('image file'), upload_to='media_assets/%Y/%m/')
    file_type = models.CharField(_('file type'), max_length=10, choices=MediaType.choices, default=MediaType.IMAGE)
    alt_text = models.CharField(
        _('alt text'),
        max_length=255,
        blank=True,
        help_text=_('Enforced mandatory field before an article using this image can be published.')
    )
    caption = models.TextField(_('caption'), blank=True)
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_media'
    )
    width = models.PositiveIntegerField(_('width in pixels'), null=True, blank=True)
    height = models.PositiveIntegerField(_('height in pixels'), null=True, blank=True)
    file_size = models.PositiveIntegerField(_('file size in bytes'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Media Asset')
        verbose_name_plural = _('Media Assets')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-process and convert image uploads to WebP format if image file changes."""
        if self.file and hasattr(self.file, 'file'):
            try:
                img = Image.open(self.file)
                self.width, self.height = img.size

                # Resize if max width > 1920px
                max_width = 1920
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    self.width, self.height = img.size

                # Convert to RGB/RGBA before saving as WebP
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGBA', img.size, (255, 255, 255, 0))
                    background.paste(img, (0, 0), img)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                buffer = BytesIO()
                img.save(buffer, format='WEBP', quality=85, optimize=True)
                buffer.seek(0)

                filename = os.path.splitext(os.path.basename(self.file.name))[0] + '.webp'
                self.file.save(filename, ContentFile(buffer.read()), save=False)
                self.file_size = buffer.tell()
            except Exception:
                pass

        super().save(*args, **kwargs)


class VideoPlatform(models.TextChoices):
    YOUTUBE = 'YOUTUBE', _('YouTube')
    VIMEO = 'VIMEO', _('Vimeo')
    SELF_HOSTED = 'SELF_HOSTED', _('Self Hosted')


class VideoEmbed(models.Model):
    """
    Video Embed parser model for YouTube and Vimeo embeds.
    """
    title = models.CharField(_('video title'), max_length=255)
    platform = models.CharField(_('platform'), max_length=20, choices=VideoPlatform.choices, default=VideoPlatform.YOUTUBE)
    video_url = models.URLField(_('video URL'))
    embed_id = models.CharField(_('embed ID'), max_length=100, blank=True)
    thumbnail_url = models.URLField(_('thumbnail URL'), blank=True)
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_videos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Video Embed')
        verbose_name_plural = _('Video Embeds')

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"

    def save(self, *args, **kwargs):
        """Auto-extract embed_id and thumbnail_url from YouTube / Vimeo URLs."""
        if self.video_url:
            if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
                self.platform = VideoPlatform.YOUTUBE
                match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', self.video_url)
                if match:
                    self.embed_id = match.group(1)
                    self.thumbnail_url = f"https://img.youtube.com/vi/{self.embed_id}/hqdefault.jpg"
            elif 'vimeo.com' in self.video_url:
                self.platform = VideoPlatform.VIMEO
                match = re.search(r'vimeo\.com\/(?:video\/)?([0-9]+)', self.video_url)
                if match:
                    self.embed_id = match.group(1)
        super().save(*args, **kwargs)
