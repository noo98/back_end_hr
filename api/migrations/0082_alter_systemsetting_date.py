# Generated by Django 5.1.4 on 2025-06-16 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_monthly_payment_sy_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemsetting',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
