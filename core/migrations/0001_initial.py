from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Headlines', max_length=100, verbose_name='site name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='settings/', verbose_name='site logo')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='settings/', verbose_name='site favicon')),
                ('primary_color', models.CharField(default='#1E3A8A', max_length=20, verbose_name='primary theme color')),
                ('secondary_color', models.CharField(default='#D97706', max_length=20, verbose_name='secondary accent color')),
                ('footer_text', models.TextField(default='© Headlines CMS. All rights reserved.', verbose_name='footer copyright text')),
                ('contact_email', models.EmailField(default='contact@headlines.example.com', max_length=254, verbose_name='contact email')),
                ('facebook_url', models.URLField(blank=True, verbose_name='Facebook URL')),
                ('twitter_url', models.URLField(blank=True, verbose_name='Twitter / X URL')),
                ('instagram_url', models.URLField(blank=True, verbose_name='Instagram URL')),
                ('youtube_url', models.URLField(blank=True, verbose_name='YouTube URL')),
            ],
            options={
                'verbose_name': 'Site Setting',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='HomepageLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='section title')),
                ('section_type', models.CharField(choices=[('HERO', 'Hero Main Banner & Grid'), ('TICKER', 'Breaking News Ticker'), ('FEATURED_GRID', 'Featured Stories Grid'), ('CATEGORY_ROW', 'Category Content Row'), ('LOCATION_ROW', 'Local News Row (State/City)'), ('TRENDING_LIST', 'Trending Most Read Sidebar'), ('EDITOR_PICK', "Editor's Picks Showcase")], default='HERO', max_length=20, verbose_name='section layout type')),
                ('display_order', models.PositiveIntegerField(default=0, verbose_name='display order')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='is active')),
                ('item_limit', models.PositiveIntegerField(default=5, verbose_name='items count limit')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='taxonomy.category', verbose_name='filter category')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='taxonomy.location', verbose_name='filter location')),
            ],
            options={
                'verbose_name': 'Homepage Layout Block',
                'verbose_name_plural': 'Homepage Layout Blocks',
                'ordering': ['display_order'],
            },
        ),
    ]
