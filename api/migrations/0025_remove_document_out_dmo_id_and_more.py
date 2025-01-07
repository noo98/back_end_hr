# Generated by Django 5.1.4 on 2025-01-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_document_out_id_remove_documententry_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document_out',
            name='dmo_id',
        ),
        migrations.RemoveField(
            model_name='documententry',
            name='dmt_id',
        ),
        migrations.AddField(
            model_name='document_out',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documententry',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
