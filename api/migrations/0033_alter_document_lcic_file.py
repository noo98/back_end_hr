# Generated by Django 5.1.4 on 2025-01-10 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_alter_document_lcic_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document_lcic',
            name='file',
            field=models.FileField(default=1, upload_to='documents/'),
            preserve_default=False,
        ),
    ]
