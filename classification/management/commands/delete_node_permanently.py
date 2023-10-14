from django.core.management.base import BaseCommand, CommandError
from classification.models import Node
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'This command deletes all soft deleted nodes that are 30 days and more older'

    def handle(self, *args, **options):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        soft_deleted_nodes = Node.objects.deleted().filter(updated_at__gte=thirty_days_ago)
        for node in soft_deleted_nodes:
            node.hard_delete()

        