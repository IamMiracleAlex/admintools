# Generated by Django 3.0.8 on 2020-07-14 14:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeniedUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=2000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomainPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('approximate_urls', models.PositiveIntegerField(blank=True, null=True)),
                ('views', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('red', 'red'), ('amber', 'amber'), ('green', 'green')], default='green', max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Domain Priority Queue',
                'db_table': 'domains',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(choices=[('page_products', 'page_products'), ('products_entities', 'products_entities'), ('entities_classification', 'entities_classification'), ('bad_url', 'bad_url')], default='page_products', max_length=25)),
                ('time_started', models.DateTimeField(auto_now_add=True)),
                ('time_submitted', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('step_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'steps',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=2000, unique=True)),
                ('page_views', models.PositiveIntegerField()),
                ('known', models.BooleanField(default=False)),
                ('last_counted', models.DateTimeField()),
                ('events', models.PositiveIntegerField()),
                ('annotators_assigned', models.PositiveIntegerField(default=0)),
                ('required_annotations', models.PositiveIntegerField(default=1)),
                ('archived_url', models.CharField(blank=True, max_length=2000, null=True)),
                ('status', models.CharField(choices=[('red', 'red'), ('amber', 'amber'), ('green', 'green')], max_length=5)),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='annotation.DomainPriority')),
            ],
            options={
                'db_table': 'urls',
                'ordering': ['page_views'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('in_progress', 'in_progress'), ('completed', 'completed'), ('bad_url', 'bad_url')], default='in_progress', max_length=15)),
                ('mode', models.CharField(blank=True, choices=[('developer', 'developer'), ('annotator', 'annotator')], default='annotator', max_length=10, null=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='annotation.Url')),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]