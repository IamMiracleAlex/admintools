# Generated by Django 3.1.1 on 2021-04-20 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_clientuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
    ]
