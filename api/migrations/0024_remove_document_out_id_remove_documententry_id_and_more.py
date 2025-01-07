# Generated by Django 5.1.4 on 2025-01-02 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_systemlogins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document_out',
            name='id',
        ),
        migrations.RemoveField(
            model_name='documententry',
            name='id',
        ),
        migrations.AddField(
            model_name='document_out',
            name='dmo_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documententry',
            name='dmt_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
