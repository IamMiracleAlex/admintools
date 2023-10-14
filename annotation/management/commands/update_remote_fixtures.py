import os
from datetime import datetime
from gzip import GzipFile
from timeit import default_timer as timer

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

import boto3

s3 = boto3.client("s3")
temp_file = os.path.join("/tmp/", "fixtures.json")
temp_file_zipped = os.path.join("/tmp/", "fixtures.json.gz")

class Command(BaseCommand):
    help = "Dumps content of the database to s3"

    def get_fixture_file(self):
        with open(temp_file, "w") as fixture_file:
            call_command('dumpdata', exclude=["custom_logger", "django_db_logger"], stdout=fixture_file)
            
            return fixture_file

    def compress_fixture_file(self, fixture_file):
        with open(temp_file, "rb") as fixture_file, open(temp_file_zipped, "wb") as compressed_file:
            gzip_file = GzipFile(compresslevel=9, fileobj=compressed_file)
            gzip_file.write(fixture_file.read())
            gzip_file.close()
            return compressed_file

    def upload_file(self, filename):
        with open(temp_file_zipped, "rb") as file_object:
            s3.put_object(Bucket="remote-fixtures", Key=filename, Body=file_object)

    def handle(self, *args, **options):
        if not settings.DEBUG:

            print("Generating fixtures...")
            dumpdata_start = timer()
            filename = temp_file

            fixture_file = self.get_fixture_file()
            dumpdata_end = timer()
            print(f"fixtures generated in {dumpdata_end - dumpdata_start}s")
            
            print("Compressing file...")
            fixture_file = self.compress_fixture_file(fixture_file)
            upload_start = timer()
            print("Uploading fixtures")
            self.upload_file(filename)
            upload_end = timer()
            print(f"uploaded dump in {upload_end - upload_start}s")

            print (f"{filename} uploaded successfully!")
            print(f"Total time ellapsed: {upload_end - dumpdata_start}")
            os.remove(temp_file)
            os.remove(temp_file_zipped)
        else:
            self.stdout.write(self.style.ERROR("This command is disabled for local environment"))

