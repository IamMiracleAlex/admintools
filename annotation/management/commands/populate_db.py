import json

from django.core.management.base import BaseCommand
from annotation.models import DomainPriority, Url
from django.db import IntegrityError
from django.utils import timezone


class Command(BaseCommand):
    help = 'populate DomainPriority and Url Models for testing'

    def handle(self, *args, **kwargs):

        infile = open('fixtures/url_data.json', 'r')
        json_urls = json.loads(infile.read())

        for json_url in json_urls.keys():
            try:
                currentDomain = DomainPriority.objects.get(domain=json_url)
            except DomainPriority.DoesNotExist:
                currentDomain = DomainPriority.objects.create(domain=json_url)

            domainUrls = json_urls[json_url] 
            self.populate_urls(currentDomain, domainUrls)
            
                
        print("[*] TASK COMPLETE!!!")

    def populate_urls(self, currentDomain, urls):
        # this function accepts a list of urls and loads it into the Url Model

        for url in urls:

            try:
                Url.objects.create(url=url, page_views=12333, last_counted=timezone.now(), events=1, status='amber', domain=currentDomain)
            except IntegrityError:
                continue
            
        
        print("{} have been loaded".format(currentDomain))

    