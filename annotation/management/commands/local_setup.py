from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
import json
from annotation.models import Url

class Command(BaseCommand):
    help = "migrate and populate table with initial data"
    
    def handle(self, *args, **options):
        
        if settings.ENVIRONMENT == "local":
            # run migrations
            print("Running initial migrations...")
            call_command('migrate')
            # seeding node data
            self.stdout.write(self.style.MIGRATE_HEADING("Seeding node data to db..."))
            call_command('json_to_sql')
            # populate urls
            self.stdout.write(self.style.MIGRATE_HEADING("Adding urls to db..."))
            call_command('populate_db')
            # Add urls to TBAQ
            self.stdout.write(self.style.MIGRATE_HEADING("Adding urls to TBAQ..."))
            self.load_tbaq()
            # populate facet
            self.stdout.write(self.style.MIGRATE_HEADING("Adding facets to db..."))
            call_command('populate_facets')
            # All set
            self.stdout.write(self.style.SUCCESS("All Done!!!"))
        else:
            self.stdout.write(self.style.ERROR("This command is only permitted for development environments"))
    
    def load_tbaq(self):
        with open('fixtures/tbaq.json', 'r') as f:
            tbaq = json.loads(f.read())
            for url in tbaq:
                Url.objects.filter(url=url['url']).update(
                    archived_url=url['archived_url'],
                    status=url['status'],
                )
                
        return True