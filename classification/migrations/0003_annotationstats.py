# Generated by Django 3.1.1 on 2020-10-29 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0002_auto_20201017_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Annotation Scoreboard',
            },
        ),
    ]
