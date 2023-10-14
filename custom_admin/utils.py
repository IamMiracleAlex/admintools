from config.settings import AIRFLOW_ENVIRONMENT
import requests
import boto3
import base64

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturalday

AIRFLOW_ENVIRONMENT = settings.AIRFLOW_ENVIRONMENT

def get_next_level(level): 
    LEVEL_CONSTANTS = ["department","category","subcategory","subset"]
    if level != 'subset':
        return LEVEL_CONSTANTS[LEVEL_CONSTANTS.index(level)+1]
    return None

class DagError(Exception):
    pass


def trigger_dag():
    client = boto3.client('mwaa')
    token = client.create_cli_token(Name=AIRFLOW_ENVIRONMENT)
    url = "https://{0}/aws_mwaa/cli".format(token['WebServerHostname'])
    body = 'trigger_dag pulse-subscriptions'
    headers = {
        'Authorization' : 'Bearer '+token['CliToken'],
        'Content-Type': 'text/plain'
        }
    r = requests.post(url, data=body, headers=headers)
    data = r.json()
    result = base64.b64decode(data['stdout']).decode('utf-8')
    error = base64.b64decode(data['stderr']).decode('utf-8')
    
    if error != "":
        raise DagError(error)

    return result


def format_last_run_date(date: datetime)-> str:
    natural_day = naturalday(date)
    return natural_day