# Generated by Django 5.1.4 on 2025-02-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_employee_lcic_salary_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_lcic',
            name='phone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
