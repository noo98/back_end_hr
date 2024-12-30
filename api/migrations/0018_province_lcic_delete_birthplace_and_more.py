# Generated by Django 5.1.4 on 2024-12-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_employee_lcic_education_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province_LCIC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Prov_ID', models.CharField(blank=True, max_length=50, null=True)),
                ('Province_Name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Birthplace',
        ),
        migrations.AddField(
            model_name='employee_lcic',
            name='percent_95',
            field=models.DateField(blank=True, null=True),
        ),
    ]
