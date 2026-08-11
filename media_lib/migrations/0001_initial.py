from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='asset title')),
                ('file', models.ImageField(upload_to='media_assets/%Y/%m/', verbose_name='image file')),
                ('file_type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video')], default='IMAGE', max_length=10, verbose_name='file type')),
                ('alt_text', models.CharField(blank=True, help_text='Enforced mandatory field before an article using this image can be published.', max_length=255, verbose_name='alt text')),
                ('caption', models.TextField(blank=True, verbose_name='caption')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='width in pixels')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='height in pixels')),
                ('file_size', models.PositiveIntegerField(blank=True, help_text='File size in bytes', null=True, verbose_name='file size in bytes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_media', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Media Asset',
                'verbose_name_plural': 'Media Assets',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VideoEmbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='video title')),
                ('platform', models.CharField(choices=[('YOUTUBE', 'YouTube'), ('VIMEO', 'Vimeo'), ('SELF_HOSTED', 'Self Hosted')], default='YOUTUBE', max_length=20, verbose_name='platform')),
                ('video_url', models.URLField(verbose_name='video URL')),
                ('embed_id', models.CharField(blank=True, max_length=100, verbose_name='embed ID')),
                ('thumbnail_url', models.URLField(blank=True, verbose_name='thumbnail URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_videos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Video Embed',
                'verbose_name_plural': 'Video Embeds',
            },
        ),
    ]
