# Generated by Django 5.1.4 on 2025-02-13 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_rename_roles_status_sidebar_remove_status_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='sidebar',
            name='url',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
