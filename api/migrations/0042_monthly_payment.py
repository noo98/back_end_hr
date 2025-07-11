# Generated by Django 5.1.4 on 2025-06-02 02:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_remove_overtimework_pos_id_overtimework_emp_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthly_payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('emp_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.employee_lcic')),
                ('fue_subsidy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.fuelsubsidy')),
                ('ot_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.overtimework')),
            ],
        ),
    ]
