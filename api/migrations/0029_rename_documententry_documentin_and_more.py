# Generated by Django 5.1.4 on 2025-01-03 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_rename_id_document_out_dmo_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentEntry',
            new_name='Documentin',
        ),
        migrations.RenameModel(
            old_name='Document_out',
            new_name='Documentout',
        ),
    ]
