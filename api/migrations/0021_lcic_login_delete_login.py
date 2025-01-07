# Generated by Django 5.1.4 on 2024-12-30 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='LCIC_Login',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user_login',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Login',
        ),
    ]
