# Generated by Django 5.1.4 on 2025-06-11 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_rename_job_mobility_policy_colpolicy_history_jm_policy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colpolicy_history',
            old_name='total_paymant',
            new_name='total_payment',
        ),
    ]
