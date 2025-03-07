# Generated by Django 5.1.4 on 2025-02-12 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_remove_sidebar_icon_remove_sidebar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='icon',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='status_roles', to='api.sidebar'),
        ),
        migrations.AddField(
            model_name='status',
            name='url',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
