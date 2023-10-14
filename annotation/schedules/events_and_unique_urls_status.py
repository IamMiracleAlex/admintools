import datetime
import os
from pathlib import Path
import csv

import boto3
import requests
from celery import shared_task

from admintool.models import DataStatus


s3_resource = boto3.resource('s3')
bucket_name = "centricity-daily-impact"
base_dir = "/tmp/"


@shared_task
def handle():
    """Process daily events and unique urls"""


    def process_data(remote_directory):

        local_directory = download_s3_directory(
                bucket_name = bucket_name,
                remote_directory = remote_directory
        )
        pathlist = Path(local_directory).rglob('*.csv')
        for path in pathlist:
            with open(path, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    DataStatus.objects.create(name=row[0], value=row[1])

        print("Data processed successfully")
                    

    def download_s3_directory(bucket_name, remote_directory):
        
        print("Collecting data from: ", remote_directory)
        bucket = s3_resource.Bucket(bucket_name) 

        for obj in bucket.objects.filter(Prefix=remote_directory):
         
            if not os.path.exists(os.path.dirname(base_dir + obj.key)):
                os.makedirs(os.path.dirname(base_dir + obj.key))

            if not obj.key == remote_directory: 
                file_name = obj.key
                if file_name.endswith(".csv"):
                    bucket.download_file(obj.key, base_dir + obj.key) 
            
        print("dowmload successful")       
        local_directory = base_dir + remote_directory
        return local_directory

        
    t = datetime.datetime.now() - datetime.timedelta(days=2)
    year, month, day = t.strftime('%Y'), t.strftime('%m'), t.strftime('%d')
    
    print("processing events")
    process_data(remote_directory=f"events/yyyy={year}/mm={month}/dd={day}")

    print("Processing Unique urls")
    process_data(remote_directory=f"unique-urls/yyyy={year}/mm={month}/dd={day}")
