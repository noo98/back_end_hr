# Generated by Django 5.1.4 on 2025-02-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_employee_lcic_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_lcic',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
