# Generated by Django 5.1.4 on 2024-12-18 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userlogin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_myapp_lcic',
            fields=[
                ('emp_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=10)),
                ('name_E', models.CharField(max_length=100)),
                ('name_L', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('employment_date', models.DateField()),
                ('percent_95', models.DateField()),
                ('youth_reserve', models.DateField()),
                ('youth_full', models.DateField()),
                ('labor_union', models.DateField()),
                ('phone', models.CharField(max_length=15)),
                ('home_address', models.CharField(max_length=255)),
                ('current_address', models.CharField(max_length=255)),
                ('education_level', models.CharField(max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('salary_grade', models.CharField(max_length=50)),
                ('employment_years', models.IntegerField()),
            ],
        ),
    ]