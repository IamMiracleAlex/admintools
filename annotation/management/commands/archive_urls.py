import time, json
import requests
from django.db.models import F, Q
from django.core.management.base import BaseCommand
from annotation.models import Url, DomainPriority


class Command(BaseCommand):
    help = 'Fetch archives for urls'

    def handle(self, *args, **kwargs):

        tbaq = Url.objects.filter(status="green", known=False).filter(Q(archived_url = None) |Q(archived_url = 'None'))

        if not tbaq.exists():
            # No whitelisted url to archive? start archiving urls from top 10 domains.
            top_ten_domains = [domain for domain in DomainPriority.objects.all()[:10]]

            tbaq =  Url.objects.filter(
                known=False,
                domain__in=top_ten_domains,
                archived_url = None, 
                annotators_assigned__lt=F("required_annotations")
                ).filter(Q(archived_url = None) |Q(archived_url = 'None'))[:200]

        if tbaq:
            for url in tbaq:
                print(f"Getting archive for {url.url}...")
                self.url_to_internet_archive(url)
        else:
            print("Nothing to do here...")

    def url_to_internet_archive(self, new_url):
        save_endpoint = "https://chrome-api.archive.org/"
        archived_endpoint = "http://web.archive.org/"
        combined_endpoint = save_endpoint + new_url.url
        try:
            r = requests.get(combined_endpoint)
            #print(r.headers)
            content_location = r.headers.get("content-location")
            cache_key = r.headers.get("x-cache-key")
            link = r.headers.get("link").split(',')[3].split(';')
            if link:
                archived_url = link[0]
            
            if content_location:
                archived_url = archived_endpoint + content_location

            elif cache_key:
    #             LOOKS LIKE:
    #             "httpweb.archive.org/web/20200713175606/https://www.allrecipes.com/recipe/231664/sweet-teriyaki-beef-skewers/US"
                remove_front = cache_key.split("httpweb.archive.org/web/")
                archived_url = archived_endpoint + remove_front[1][:-3]
            new_url.archived_url = archived_url
            new_url.save()
        except requests.exceptions.HTTPError as e:
            return e.response.text