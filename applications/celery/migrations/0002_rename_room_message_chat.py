# Generated by Django 3.2.9 on 2021-12-13 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room',
            new_name='chat',
        ),
    ]
