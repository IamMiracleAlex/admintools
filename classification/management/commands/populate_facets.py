import json
from django.conf import settings
from django.core.management.base import BaseCommand
from classification.models import FacetCategory, FacetValue

class Command(BaseCommand):
    help = 'Populates rds with with facets'

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            with open("fixtures/facets.json", "r") as facet_data:
                facet_categories = json.load(facet_data)
                for category in facet_categories:
                    print(f"Adding {category['title']}")
                    category_object = FacetCategory.objects.create(title=category["title"], description=category["description"])
                    for facet in category["facets"]:
                        FacetValue.objects.create(
                            label=facet["label"], category=category_object, description=facet["description"])
