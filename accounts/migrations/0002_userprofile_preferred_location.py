from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='preferred_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_by_profiles', to='taxonomy.location', verbose_name='preferred location'),
        ),
    ]
