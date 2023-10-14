# Generated by Django 3.0.8 on 2020-10-28 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0012_auto_20201016_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeeswaxList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='domainpriority',
            name='status',
            field=models.CharField(choices=[('red', 'red'), ('amber', 'amber'), ('green', 'green')], default='amber', max_length=5),
        ),
        migrations.CreateModel(
            name='ClientDomainRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('red', 'red'), ('amber', 'amber'), ('green', 'green')], default='amber', max_length=50)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.Client')),
                ('domain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.DomainPriority')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='beeswax_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='annotation.BeeswaxList'),
        ),
        migrations.AddField(
            model_name='client',
            name='domains',
            field=models.ManyToManyField(blank=True, through='annotation.ClientDomainRelationship', to='annotation.DomainPriority'),
        ),
    ]
