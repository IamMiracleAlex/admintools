# Generated by Django 3.1.1 on 2021-01-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0027_taskbreakdown'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueurlrelationship',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
