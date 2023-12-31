# Generated by Django 2.2 on 2020-05-29 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DecimalField(decimal_places=2, max_digits=4)),
                ('time', models.DateTimeField(auto_now=True)),
                ('request_url', models.URLField()),
                ('request_querystring', models.TextField()),
                ('request_body', models.TextField()),
                ('response_body', models.TextField()),
                ('request_method', models.CharField(max_length=10)),
                ('request_headers', models.TextField()),
                ('response_status', models.CharField(max_length=4)),
            ],
        ),
    ]
