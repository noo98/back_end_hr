# Generated by Django 5.1.4 on 2024-12-13 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
