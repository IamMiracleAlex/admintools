from django.core.management import BaseCommand
from custom_logger.models import RequestLog
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help='clears Request Logs older than 30 days'

    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - timedelta(days=30)
        old_logs = RequestLog.objects.filter(time__lte=time_threshold)
        count = len(old_logs)
        #time__gte is django's magic way of saying time is greater than or equal to
        old_logs.delete()

        print("{} stale Logs cleared!".format(count))
        print("TASK COMPLETE!")
        

