# Generated by Django 5.1.4 on 2025-06-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_rename_hd_mor_after_overtimework_hd_mor_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='SalaryGrade',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]
