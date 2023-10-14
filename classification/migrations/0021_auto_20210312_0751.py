# Generated by Django 3.1.1 on 2021-03-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0020_merge_20210311_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedNode',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Recently deleted nodes',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('classification.node',),
        ),
        migrations.AlterField(
            model_name='node',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('deleted', 'deleted')], default='active', max_length=50),
        ),
    ]