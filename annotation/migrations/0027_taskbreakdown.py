# Generated by Django 3.1.1 on 2021-01-26 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0026_auto_20210126_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskBreakdown',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('annotation.task',),
        ),
    ]