# Generated by Django 3.1.1 on 2021-03-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0017_merge_20210309_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facetcategory',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='facetcategory',
            name='facet_type',
            field=models.CharField(blank=True, choices=[('single', 'single'), ('multi', 'multi'), ('boolean', 'boolean')], default='boolean', max_length=100),
        ),
        migrations.AlterField(
            model_name='facetvalue',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='nodefacetrelationship',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
