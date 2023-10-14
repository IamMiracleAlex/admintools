# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/
import json
import boto3
import os
from botocore.exceptions import ClientError
def get_secret():
    secret = {}
    secret_name = os.environ.get('SECRET_MANAGER_NAME', 'dev-test-secret')
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret =  json.loads(secret_value_response["SecretString"])

    except ClientError as e:
        print(e)

    return secret
