# Generated by Django 3.1.1 on 2020-10-27 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_queue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
