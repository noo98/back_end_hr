# Generated by Django 5.1.4 on 2025-02-13 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_alter_document_lcic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document_lcic',
            name='status',
            field=models.CharField(choices=[('new', 'ໃໝ່'), ('viewed', 'ເບີ່ງແລ້ວ')], default='new', max_length=10),
        ),
    ]
