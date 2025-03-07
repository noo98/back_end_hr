# Generated by Django 5.1.4 on 2025-02-20 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0097_delete_documentreadstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document_Status',
            fields=[
                ('docstat_id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('doc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.document_lcic')),
                ('us_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.systemuser')),
            ],
        ),
    ]
