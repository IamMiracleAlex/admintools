# Generated by Django 3.1.1 on 2021-06-15 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0044_auto_20210604_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]