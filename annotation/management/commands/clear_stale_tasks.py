from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db.models import F
from annotation.models import Task


class Command(BaseCommand):
    help = 'Management command to unassign stale tasks'

    def handle(self, *args, **kwargs):
        stale_tasks = Task.objects.filter(
            #Start date is more than 14 days ago
            start_date__gt= F("start_date")+timedelta(days=14),
            completed = False
        )
        if stale_tasks.exists():
            print(f"{stale_tasks.count()} tasks found!")

            #AWS may time out long running tasks. We need to know how
            #many stale tasks was successfully unassigned
            count = 0
            for task in stale_tasks:
                url = task.url
                url.annotators_assigned -= 1
                url.save()
                task.delete()
                count += 1
            print(f"{count} stale tasks cleared!")
        print("TASK COMPLETE!")


