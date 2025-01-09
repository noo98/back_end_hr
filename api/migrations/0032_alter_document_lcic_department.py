# Generated by Django 5.1.4 on 2025-01-08 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_document_lcic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document_lcic',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.department'),
            preserve_default=False,
        ),
    ]
