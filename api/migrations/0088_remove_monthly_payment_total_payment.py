# Generated by Django 5.1.4 on 2025-06-20 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_saving_cooperative_loan_deduction_194_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthly_payment',
            name='total_payment',
        ),
    ]
