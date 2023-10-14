from datetime import timedelta

from django.utils import timezone
from django_db_logger.models import StatusLog
from django_celery_results.models import TaskResult

from celery import shared_task

from custom_logger.models import RequestLog, ChromeExtensionLog


@shared_task
def clear_old_request_logs():
    'clears Request Logs older than 14 days'
    
    time_threshold = timezone.now() - timedelta(days=14)
    old_logs = RequestLog.objects.filter(time__lte=time_threshold)
    count = len(old_logs)
    #time__gte is django's magic way of saying time is greater than or equal to
    old_logs.delete()

    print("{} stale Logs cleared!".format(count))
    print("TASK COMPLETE!")


@shared_task
def clear_old_chrome_extension_logs():
    'clears ChromeExtensionLog Logs older than 30 days'
    
    time_threshold = timezone.now() - timedelta(days=30)
    old_logs = ChromeExtensionLog.objects.filter(created_at__lte=time_threshold)
    count = len(old_logs)
    #time__gte is django's magic way of saying time is greater than or equal to
    old_logs.delete()

    print("{} stale Logs cleared!".format(count))
    print("TASK COMPLETE!")


@shared_task
def clear_old_database_logs():
    'clears ChromeExtensionLog Logs older than 30 days'
    
    time_threshold = timezone.now() - timedelta(days=30)
    old_logs = StatusLog.objects.filter(create_datetime__lte=time_threshold)
    count = len(old_logs)
    #time__gte is django's magic way of saying time is greater than or equal to
    old_logs.delete()

    print("{} stale Logs cleared!".format(count))
    print("TASK COMPLETE!")


@shared_task
def clear_old_celery_result_logs():
    'clears TaskResult Logs older than 30 days'
    
    time_threshold = timezone.now() - timedelta(days=30)
    old_logs = TaskResult.objects.filter(date_created__lte=time_threshold)
    count = len(old_logs)
    #time__gte is django's magic way of saying time is greater than or equal to
    old_logs.delete()

    print("{} stale Logs cleared!".format(count))
    print("TASK COMPLETE!")