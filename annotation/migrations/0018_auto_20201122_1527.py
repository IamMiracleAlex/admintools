# Generated by Django 3.1.1 on 2020-11-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0017_auto_20201122_0753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facetproperty',
            options={'verbose_name_plural': 'Facet properties'},
        ),
        migrations.AddField(
            model_name='intentdata',
            name='facets',
            field=models.JSONField(default=[]),
        ),
    ]
