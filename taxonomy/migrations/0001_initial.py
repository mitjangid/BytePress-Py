from django.db import migrations, models
import django.db.models.deletion
import mptt.fields

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='category name')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('icon', models.CharField(blank=True, help_text="FontAwesome or CSS icon class e.g., 'fa-globe'", max_length=50, verbose_name='icon class')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='is active')),
                ('display_order', models.PositiveIntegerField(default=0, verbose_name='display order')),
                ('meta_title', models.CharField(blank=True, help_text='Custom SEO page title override.', max_length=150, verbose_name='meta title')),
                ('meta_description', models.TextField(blank=True, help_text='Custom SEO meta description override.', verbose_name='meta description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='taxonomy.category', verbose_name='parent category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='location name')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='slug')),
                ('location_type', models.CharField(choices=[('STATE', 'State / Region'), ('CITY', 'City')], default='STATE', max_length=10, verbose_name='location type')),
                ('state_code', models.CharField(blank=True, help_text='e.g. CA, NY, TX', max_length=10, verbose_name='state code')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='longitude')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='taxonomy.location', verbose_name='parent state / region')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ['name'],
            },
        ),
    ]
