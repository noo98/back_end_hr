# Generated by Django 5.1.4 on 2025-02-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_employee_lcic_years_of_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_lcic',
            name='salary_level',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
