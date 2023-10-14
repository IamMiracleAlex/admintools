import boto3
import csv
import codecs

from django.core.management.base import BaseCommand
from annotation.models import IntentData, Url

s3 = boto3.client("s3")


class Command(BaseCommand):
    help = "Backfills the csv of urls that were annotated from s3"

    def handle(self, *args, **kwargs):
        bucket = "known-urls"
        # s3 returns only 1000 objects per request so we paginate
        paginator = s3.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=bucket)
        for page in result:
            if "Contents" in page:
                # find the csv for each url
                for key in page["Contents"]:
                    keyString = key["Key"]
                    obj = s3.get_object(Bucket=bucket, Key=keyString)
                    csv_file = codecs.getreader("utf-8")(obj["Body"])
                    fieldnames = ["url", "department", "category", "subcategory", "subset", "intent"]
                    reader = csv.DictReader(csv_file, fieldnames=fieldnames)

                    data = list(reader)
                    csv_url = data[0]["url"]

                    try:
                        # get the url for the csv file
                        url_obj = Url.objects.get(url=csv_url)

                        # Check if intent data already exist for this url
                        intent_data = url_obj.intent_data.all()
                        if not intent_data.exists():

                            # loop throught the entities in the csv file
                            print(f"Adding Intent Data for {csv_url}")
                            for entity in data:

                                url_obj.intent_data.create(
                                    department=entity["department"],
                                    category=entity["category"],
                                    subcategory=entity["subcategory"],
                                    subset=entity["subset"],
                                    intent=entity["intent"])
                        else:
                            print("Intent Data already exists for this url")
                    except Exception as e:
                        print(e)
