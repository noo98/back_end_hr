# Generated by Django 5.1.4 on 2025-06-16 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0080_overtime_history_emp_name_overtime_history_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_payment',
            name='sy_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.subsidyyear'),
        ),
    ]
