# Generated by Django 5.1.4 on 2024-12-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
