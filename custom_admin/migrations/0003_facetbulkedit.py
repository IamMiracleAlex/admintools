# Generated by Django 3.1.1 on 2021-04-21 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0002_auto_20201201_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacetBulkEdit',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Facet Bulk Edit',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('custom_admin.bulkedit',),
        ),
    ]
