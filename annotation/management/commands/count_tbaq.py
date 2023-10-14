import json
import requests
from django.core.management.base import BaseCommand
from annotation.models import Url


class Command(BaseCommand):
    help = 'Count number of items left in annotation queue'

    def handle(self, *args, **kwargs):
        count = Url.objects.tbaq().count()
        print(f"{count} urls left in annotation queue")

        if count < 50:
            #Notify on slack
            #TODO: Make request async
            data = {"payload": json.dumps({"text": f"Annotation queue is running low!\n {count} urls left"})}
            webhook_url = "https://hooks.slack.com/services/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"

            r = requests.post(webhook_url, data=data)


