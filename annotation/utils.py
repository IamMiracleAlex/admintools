import csv
import io
import re
import random
import string

from django.http import HttpResponse

import boto3
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from langdetect import detect

s3_resource = boto3.resource('s3')
s3 = boto3.client("s3")


def send_csv_to_s3(url, csv, filename="entities.csv"):
    """
    Uploads the generated csv data to know-urls bucket on s3
    as url/entities.csv
    """
    clean_url = re.sub("^.*?://", "", url)
    if not clean_url[-1] == "/":
        clean_url += "/"
    file_name = f"{clean_url}{filename}"
    s3.put_object(Bucket="known-urls", Key=file_name, Body=csv)


def data_to_csv(data:list, fieldnames=None):
    """
    This is a replacement to pandas dataframe.to_csv to create
    csv files from a list of dictionaries and stored in memory (no file is created)
    because i hate how we install the entire pandas(which in turn installs numpy)
    library just to use dataframe.to_csv
    """ 
    file_ = io.StringIO()

    #auto infer fieldnames if not provided
    if not fieldnames:
        fieldnames = data[0].keys()

    csv.DictWriter(file_, fieldnames).writerows(data)

    return file_.getvalue()


def randomString(stringLength=30):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return " ".join(t.strip() for t in visible_texts)


def verify_lang(url):
    html = requests.get(url).text
    words = text_from_html(html)
    try:
        lang = detect(words[:500])
    except Exception as e:
        lang = None
        print("Couldn't obtain language because:", e)    
    print(lang)
    return lang   


class ExportCsvMixin:
    def export_items_to_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name != 'password']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        [writer.writerow([getattr(obj, field) for field in field_names]) for obj in queryset]                           
        return response

