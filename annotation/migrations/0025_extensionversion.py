# Generated by Django 3.1.1 on 2021-01-14 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0024_urlscraped'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtensionVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
