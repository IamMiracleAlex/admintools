# Generated by Django 3.1.1 on 2021-02-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0029_auto_20210130_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now=True)),
            ],
        ),
    ]
