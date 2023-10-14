import json

from django.core.management.base import BaseCommand

import requests

from annotation import models
from annotation.utils import verify_lang
from internet_archive.models import ArchiveSetting



class Command(BaseCommand):
    help = 'For archiving urls'

    def handle(self, *args, **kwargs):
        #archives specified number of urls at each invocation

        data = self.get_urls()

        if data['urls']:
            urls = data['urls']
            method = data['method']

            for url in urls:
                print(f"Fetching archive for {url}")
                self.url_archiver(method=method, url=url)

        else:
            print("No url to archive at this time")


    def get_urls(self):
        # get urls to be archived
        tbaq = models.Url.objects.filter(status="green", known=False, archived_url="").order_by('archive_attempt_count')
        archive_setting = ArchiveSetting.objects.first()
        number_of_urls = archive_setting.number_of_urls

        if tbaq:
            urls = []
            for url in tbaq[:number_of_urls]:
                urls.append(url.url)
                url.archive_attempt_count += 1
                url.save()
            data = {
                "urls": urls,
                'method': archive_setting.archive_method,
                }
            return data
        else:
            return "No url to archive at this time"
        

    def post_archive(self, url, archived_url):
        """
        Updates the url
        """
        models.Url.objects.filter(url=url).update(archived_url=archived_url)

     
    def internal_archive(self, url):
        # fetch internal archive 
        resp = requests.get(f'http://archive.centricity.cloud/centricity-web-archive/record/{url}')
        archived_url = None

        if resp.status_code == 200:
            print(f"Fetching internal archive for: {url}")
            headers = resp.headers  
            links = headers['Link'].split()
            new_link = list(links[7])

            unwanted = ['<', '>', ';']
            new_link = [e for e in new_link if e not in unwanted]
            archived_url  = ''.join(new_link) 
            archived_url = archived_url.replace('centricity-web-archive/record', 'live')

            print(f"New internally archived url is: {archived_url}")
        else:
            print(f"Internal archive failed..!, With status code: {resp.status_code}")

        return archived_url    


    def wayback_machine(self, url):
        save_endpoint = "https://web.archive.org/save/"
        archived_endpoint = "http://web.archive.org/web/"
        combined_endpoint = save_endpoint + url
        archived_url = None

        try:
            r = requests.get(combined_endpoint)
        except Exception as e:
            print(f"Request to {combined_endpoint} failed: {e}")
            return

        print(r.headers)
        content_location = r.headers.get("content-location", None)
        cache_key = r.headers.get("x-cache-key", None)
        
        if content_location:
            archived_url = archived_endpoint + content_location

        elif cache_key:
            #Cache key looks like: "httpsweb.archive.org/web/20201019134748/https://www.lawnmowerforum.com/threads/jd-z425-w-b/NG",
            remove_front = cache_key.split("httpsweb.archive.org/web/")[1]
            archive_number = remove_front.split("/")[0]
            archived_url = f"{archived_endpoint}{archive_number}/{url}"

        else:
            print(f"Unable to get archive for {url} using Wayback Machine")

        return archived_url


    def default_archive(self, url):
        archived_url = None

        lang = verify_lang(url)
        if lang == "de":
            print("Archiving german url")
            # german url, hence use internal archive
            archived_url = self.internal_archive(url)

        else:
            archived_url = self.wayback_machine(url)

            if not archived_url:
                archived_url = self.internal_archive(url)

        return archived_url


    def url_archiver(self, method, url):
        if method == 'internal_tool':
            archived_url = self.internal_archive(url)
        
        elif method == 'wayback_machine':
            archived_url = self.wayback_machine(url)
        
        else:
            archived_url = self.default_archive(url)
        
        if archived_url:
            self.post_archive(url, archived_url=archived_url)
