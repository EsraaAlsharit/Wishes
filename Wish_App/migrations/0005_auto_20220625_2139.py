# Generated by Django 3.2 on 2022-06-25 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Wish_App', '0004_granted_user_wish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='granted',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='wish',
            name='user',
        ),
        migrations.DeleteModel(
            name='Granted',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
    ]
