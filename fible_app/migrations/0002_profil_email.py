# Generated by Django 4.0.6 on 2022-07-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fible_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
    ]