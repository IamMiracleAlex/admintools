from rest_framework import serializers
from .adapter import Google, register_client_user
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .utils import get_user_domain
from annotation.models import Client

class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True)

   
    def validate(self, data):
        auth_token = data.get("auth_token")
        user_data = Google.validate(auth_token)
        user_email = user_data.get("email")
        user_domain = get_user_domain(user_email)
        try:
            Client.objects.get(domain_name=user_domain)
        except Client.DoesNotExist:
            raise serializers.ValidationError(f"Client with domain name {user_domain} not found")
        return data
