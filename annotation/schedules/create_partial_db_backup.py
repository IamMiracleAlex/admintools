import sys

from django.apps import apps
from django.core import serializers
from django.conf import settings

from celery import shared_task

ENVIRONMENT = settings.ENVIRONMENT


def migrate(model, dest_db, size=2000, start=0, old_db="default"):
    count = model.objects.using(old_db).count()
    print("%s objects in model %s" % (count, model))
    for i in range(start, count, size):
        print(i),
        sys.stdout.flush()
        original_data =  model.objects.using(old_db).all()[i:i+size]
        original_data_json = serializers.serialize("json", original_data)
        new_data = serializers.deserialize("json", original_data_json, 
                                           using=dest_db)
        for n in new_data:
            n.save(using=dest_db)

    print('copied all for: ', model)


def handler_(dest_db=None):
    if ENVIRONMENT in ['local', 'dev', 'staging']:
        return

    desired_apps = ['annotation', 'classification', 'subscription', 'priority_action']
    excluded_models = ['DomainLog', 'BeeswaxList', 'ExtensionVersion']
    desired_models = []

    for app in desired_apps:
        models = apps.all_models[app].values() 
        for model in models:
            if not model.__name__.startswith('Historical') and not model._meta.proxy and model.__name__ not in excluded_models:
                desired_models.append(model)

    for model in desired_models:
        migrate(model, dest_db)


@shared_task
def partial_backup_for_dev():
    dest_db = 'dev'
    handler_(dest_db=dest_db)


@shared_task
def partial_backup_for_staging():
    dest_db = 'staging'
    handler_(dest_db=dest_db)    