import io
import boto3
import gzip
import os
import random
import string

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

s3 = boto3.resource("s3")
bucket = s3.Bucket('remote-fixtures')

random_string = ''.join(random.choice(string.ascii_letters) for i in range(5))
temp_file = os.path.join("/tmp/", f"fixtures{random_string}.json")
temp_file_zipped = os.path.join("/tmp/", "fixtures.json.gz")


class Command(BaseCommand):
    help = "Populates your local database with a replica from s3"

    def decompress_file(self):
        print("Decompressing fixture_dump.json.gz > fixture.json")
        with open(temp_file, "w") as decompressed_file, gzip.open(temp_file_zipped, "rb") as gzip_file:
            with io.TextIOWrapper(gzip_file, encoding='utf-8') as decoder:
                decompressed_file.write(decoder.read())
                return decompressed_file

    def load_fixture(self, fixture_file):
        call_command('loaddata', temp_file)

    def handle(self, *args, **options):
        if settings.DEBUG:
            fixture_key = "fixture_dump.json.gz"

            # download file
            print("Downloading fixture_dump.json.gz... <This may take several minutes>")
            bucket.download_file(fixture_key, temp_file_zipped)

            # decompress
            fixture_file = self.decompress_file()
            
            # load it in
            print("Seeding database...")
            self.load_fixture(fixture_file)
            os.remove(temp_file)
            os.remove(temp_file_zipped)
        else:
            self.stdout.write(self.style.ERROR("This command is disabled for production environment"))