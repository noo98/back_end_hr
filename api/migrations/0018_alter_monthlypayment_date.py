# Generated by Django 5.1.4 on 2025-05-19 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_systemuser_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlypayment',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
