# Generated by Django 3.1.1 on 2021-01-30 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0028_queueurlrelationship_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facetproperty',
            old_name='intent',
            new_name='entity_intent',
        ),
        migrations.RenameField(
            model_name='intentdata',
            old_name='entity_intent',
            new_name='intent',
        ),
        migrations.RemoveField(
            model_name='intentdata',
            name='facet_intent',
        ),
        migrations.AddField(
            model_name='facetproperty',
            name='facet_intent',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
