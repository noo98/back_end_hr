# Generated by Django 5.1.4 on 2025-05-20 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_fuelsubsidy_total_fuel'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelsubsidy',
            name='update_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
