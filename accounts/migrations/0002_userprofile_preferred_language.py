from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(default='en', help_text='Persistent reader language preference (e.g. en, hi, mr).', max_length=10, verbose_name='preferred language'),
        ),
    ]
