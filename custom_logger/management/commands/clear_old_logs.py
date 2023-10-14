from django.core.management.base import BaseCommand
from custom_logger.models import RequestLog
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'This command deletes all Request logs older than 30 days'

    def handle(self, *args, **options):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_logs = RequestLog.objects.filter(time__gte=thirty_days_ago).delete()
        print(old_logs) #Show number of rows affected