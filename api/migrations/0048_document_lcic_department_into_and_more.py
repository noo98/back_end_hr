# Generated by Django 5.1.4 on 2025-01-31 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_remove_systemuser_status_systemuser_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='document_lcic',
            name='department_into',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='document_lcic_department_into', to='api.department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document_lcic',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_lcic_department', to='api.department'),
        ),
    ]
