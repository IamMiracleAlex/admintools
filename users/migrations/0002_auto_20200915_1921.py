# Generated by Django 3.0.8 on 2020-09-15 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('developer', 'developer'), ('annotator', 'annotator'), ('manager', 'manager'), ('machine', 'machine')], max_length=10),
        ),
    ]