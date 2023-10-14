import os
import time
import json

from django.conf import settings

import requests
from celery import shared_task

from annotation.models import DomainPriority, BeeswaxList, ClientDomainRelationship, Client


@shared_task
def handle():

    'Send greenlisted/redlisted domains to beeswax'

    details = {}

    # Get all redlisted and greenlisted domains
    redlisted_domains = [domain.domain for domain in DomainPriority.objects.filter(status="red")]
    greenlisted_domains = [domain.domain for domain in DomainPriority.objects.filter(status="green")]

    # Store redlisted/greenlisted domains with their beeswax ids
    details['Redlist'] = [redlisted_domains, 3] #their real id's from beeswax
    details['Greenlist'] = [greenlisted_domains, 1]

    # Generate greenlisted domains, with regards to available lists -- dynamically 
    # Generate redlisted domains, with regards to available lists, and clients (all clients in a list must redlist) -- dynamically 
    for list in BeeswaxList.objects.all():

        # Number of clients in a list
        client_list_count = Client.objects.filter(beeswax_list=list).count()

        # Generate greenlisted domains, and their beeswax ids with regards to available lists -- dynamically 
        details[f'{list}_greenlist'] = [[relation.domain.domain for relation in ClientDomainRelationship.objects.filter(status='green', client__beeswax_list=list)], list.greenlist_id]

        # Get all domains in a list WITHOUT duplicate
        distinct_listed_domains = ClientDomainRelationship.objects.filter(client__beeswax_list=list).distinct('domain')

        # For each of these domains, check if they were redlisted by all clients, if true
        # generate redlists, with beeswax ids for individual lists dynamically
        for relation in distinct_listed_domains:
            queryset = ClientDomainRelationship.objects.filter(domain=relation.domain, status='red')
            if queryset.count() == client_list_count:
                details[f'{list}_redlist'] = [[], list.redlist_id]
                details[f'{list}_redlist'][0].append(queryset.first().domain.domain)
   

    def upload_to_s3(domain_list, list_name, list_id):
       
        # prevent API crash when list_id is `None` or 0
        if not list_id: 
           print('Please use a valid beeswax `list id` for:', list_name)
           return

        # create and store file on temporary storage
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"{list_name}_{timestamp}.csv"
        temp_file_path = os.path.join("/tmp/", file_name)

        # populate file with domain data
        with open(temp_file_path, 'w') as temp_file:
            temp_file.writelines(domain_list)  
 
        # authenticate with beeswax and store cookies
        auth_url = 'https://centricity.api.beeswax.com/rest/authenticate'
        auth_dict = {
            "email": "miracle.alex@centricityinsights.com",
            "password": settings.SECRETS.get('BEESWAX_MIRACLE_PASSWORD')
        }
        r = requests.post(auth_url,data=json.dumps(auth_dict))
        cookies = r.cookies

        # upload file to beeswax using list ids
        files = {
            'list_item': (temp_file_path, open(temp_file_path, 'rb')),
        }
        response = requests.post(f'https://centricity.api.beeswax.com/rest/list_item_bulk/upload/{list_id}', cookies=cookies, files=files)

        print(response.text)
        print('The processed list is:', list_name)


    # upload all dynamically generated lists stored in `details`
    for key, value in details.items():
        upload_to_s3("\n".join(value[0]), key, value[1])
