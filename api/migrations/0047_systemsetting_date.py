# Generated by Django 5.1.4 on 2025-06-04 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_alter_document_format_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
