# Generated by Django 5.1.4 on 2025-02-11 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_alter_personalinformation_dob_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecializedEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=255)),
                ('inst', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('dom_abrd', models.CharField(max_length=50)),
                ('per_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.personalinformation')),
            ],
        ),
    ]
