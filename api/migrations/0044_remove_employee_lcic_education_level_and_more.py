# Generated by Django 5.1.4 on 2025-01-30 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_systemuser_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_lcic',
            name='Education_level',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='age',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='birth_place',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='current_address',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='date_95_percent',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='date_full_party',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='date_support_party',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='date_theory_training',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='emergency_contact',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='ethnicity',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='female_member',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='graduated_from',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='join_date',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='party_training',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='perm_date',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='position',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='salary_grade',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='study_sponsor',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='union_member',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='years_party',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='years_service',
        ),
        migrations.RemoveField(
            model_name='employee_lcic',
            name='youth_member',
        ),
    ]
