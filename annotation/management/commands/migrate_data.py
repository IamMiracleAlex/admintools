from django.core.management.base import BaseCommand
from annotation import models
from django.core.paginator import Paginator


class Command(BaseCommand):
    help = 'Migrate current url data to country table'

    def handle(self, *args, **kwargs):
        all_urls = models.Url.objects.all()

        country, _ = models.Country.objects.get_or_create(
                    name='US-East',
                    short_name='U.S.A',
            )
        paginator = Paginator(all_urls, 100000) # chunks of 100000

        for page_idx in range(1, paginator.num_pages):
            print(page_idx)
            for url in paginator.page(page_idx).object_list:

                models.QueueUrlRelationship.objects.get_or_create(
                    country=country, 
                    events=url.events,
                    page_views=url.page_views,
                    url=url,
                )


        print('Country table was populated successfully')

