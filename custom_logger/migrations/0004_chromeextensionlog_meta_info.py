# Generated by Django 3.1.1 on 2021-02-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_logger', '0003_chromeextensionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='chromeextensionlog',
            name='meta_info',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]