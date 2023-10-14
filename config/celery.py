import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# crontabs
app.conf.update(
    timezone='Africa/Lagos',
    enable_utc=True,
)

app.conf.beat_schedule = {
      
    "update_labelled_urls": {
        "task": "annotation.schedules.update_labelled_urls.handle",
        "schedule": crontab(minute=0, hour=0)  # every day at midnight
    },    
    "events_and_unique_urls_status": {
        "task": "annotation.schedules.events_and_unique_urls_status.handle",
        "schedule": crontab(minute=0, hour=0)  # every day at midnight
    },    
    "rds_internet_archive": {
        "task": "annotation.schedules.rds_internet_archive.handle",
        "schedule": crontab(minute='*/15')  # every 15 mins
    },    
    "delete_node_permanently": {
        "task": "classification.schedules.delete_node_permanently.handle",
        'schedule': crontab(minute=0, hour=0, day_of_month=(2, 15)),  # every 2nd and 15th of the month
    },    
    "clear_old_request_logs": {
        "task": "custom_logger.schedules.clear_old_logs.clear_old_request_logs",
        'schedule': crontab(minute=0, hour=0, day_of_month=(2, 15)),  # every 2nd and 15th of the month
    },
    "clear_old_chrome_extension_logs": {
        "task": "custom_logger.schedules.clear_old_logs.clear_old_chrome_extension_logs",
        'schedule': crontab(minute=0, hour=0, day_of_month=(2, 15)),  # every 2nd and 15th of the month
    },
    "clear_old_database_logs": {
        "task": "custom_logger.schedules.clear_old_logs.clear_old_database_logs",
        'schedule': crontab(minute=0, hour=0, day_of_month=(2, 15)),  # every 2nd and 15th of the month
    },
    "clear_old_celery_result_logs": {
        "task": "custom_logger.schedules.clear_old_logs.clear_old_celery_result_logs",
        'schedule': crontab(minute=0, hour=0, day_of_month=(2, 15)),  # every 2nd and 15th of the month
    },
    "create_snapshot_for_staging": {
        "task": "annotation.schedules.create_snapshots.create_snapshot_for_staging",
        'schedule': crontab(minute=0, hour=1, day_of_month=3),  # every 3rd day of the month, at 1am
    },
    "create_snapshot_for_dev": {
        "task": "annotation.schedules.create_snapshots.create_snapshot_for_dev",
        'schedule': crontab(minute=0, hour=1, day_of_month=1),  # every 1st day of the month, at 1am
    },
    "process_completed": {
        "task": "annotation.schedules.process_completed.process",
        "schedule": crontab(minute=0, hour=2)  # every day at 2am
    },
    "partial_backup_for_dev": {
        "task": "annotation.schedules.create_partial_db_backup.partial_backup_for_dev",
        'schedule': crontab(minute=0, hour=1, day_of_month=1),  # every 1st day of the month, at 1am
    },
    "partial_backup_for_staging": {
        "task": "annotation.schedules.create_partial_db_backup.partial_backup_for_staging",
        'schedule': crontab(minute=0, hour=1, day_of_month=3),  # every 3rd day of the month, at 1am
    },
}
