import os  
import json
import tarfile
import shutil

import django  
import boto3
                                                      
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")   
django.setup()   

from annotation.models import ExtensionVersion

s3 = boto3.client("s3")


def process(event, context):
    '''Extract chrome extension version from the S3 bucket (staging/prod)'''
    
    # Get the uploaded CE's information
    tmp_dir = '/tmp/' 
    bucket = event['Records'][0]['s3']['bucket']['name'] # e.g 'centricity-chrome-extension'  
    key = event['Records'][0]['s3']['object']['key'] # e.g 'centricity-chrome-extension.tgz' 
    file_dir = tmp_dir + key

    # Download CE and store on `/tmp/` and extract
    print("Downloading the chrome extension...")
    s3.download_file(bucket, key, file_dir)

    print("Extracting the file...")
    tar = tarfile.open(file_dir) 
    tar.extractall(path=tmp_dir)
    tar.close()

    print("Saving latest extension version...")
    with open("/tmp/build/manifest.json") as data:
        manifest = json.load(data)
    
    # create version
    ExtensionVersion.objects.create(version = manifest['version'])
    print("Latest version is: ", manifest['version'])

    # clean up
    print("Removing the extension files...")
    os.remove(file_dir)
    shutil.rmtree('/tmp/build')

    print("Process completed..!")       
    
process({}, {})