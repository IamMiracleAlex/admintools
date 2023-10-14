from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from classification.models import Node


@shared_task
def handle():
    'This command deletes all soft deleted nodes that are 30 days and more older'

    thirty_days_ago = timezone.now() - timedelta(days=30)
    soft_deleted_nodes = Node.objects.deleted().filter(updated_at__gte=thirty_days_ago)
    for node in soft_deleted_nodes:
        node.hard_delete()

    print(f"{soft_deleted_nodes.count()} nodes deleted")