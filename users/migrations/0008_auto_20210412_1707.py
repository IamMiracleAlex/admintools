# Generated by Django 3.1.1 on 2021-04-12 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0039_auto_20210412_1707'),
        ('users', '0007_merge_20201102_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='annotation.client'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('developer', 'developer'), ('annotator', 'annotator'), ('manager', 'manager'), ('machine', 'machine'), ('client_user', 'client_user'), ('client_admin', 'client_admin')], max_length=12),
        ),
    ]
