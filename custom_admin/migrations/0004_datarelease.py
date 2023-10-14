# Generated by Django 3.1.1 on 2021-05-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0003_facetbulkedit'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_run', models.DateTimeField(null=True)),
                ('result', models.CharField(choices=[('success', 'success'), ('failed', 'failed')], max_length=10, null=True)),
            ],
        ),
    ]
