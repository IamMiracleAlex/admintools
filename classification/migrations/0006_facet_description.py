# Generated by Django 3.1.1 on 2020-10-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0005_auto_20201025_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='facet',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]