# Generated by Django 3.1.1 on 2020-12-22 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0022_auto_20201204_1634'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='urleditor',
            options={'verbose_name_plural': 'URL Editor'},
        ),
        migrations.RemoveField(
            model_name='facetproperty',
            name='url',
        ),
        migrations.RemoveField(
            model_name='intentdata',
            name='facets',
        ),
        migrations.AddField(
            model_name='facetproperty',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facet_properties', to='annotation.intentdata'),
        ),
        migrations.AlterModelTable(
            name='facetproperty',
            table='facet_properties',
        ),
    ]
