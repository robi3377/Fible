# Generated by Django 4.0.6 on 2022-07-30 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fible_app', '0015_follow_tof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='tof',
        ),
    ]
