# Generated by Django 3.2 on 2022-06-25 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Wish_App', '0002_auto_20220625_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
    ]
