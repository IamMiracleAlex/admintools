# Generated by Django 3.1.1 on 2020-11-30 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0020_auto_20201124_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlEditor',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Url Editorc',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('annotation.url',),
        ),
    ]
