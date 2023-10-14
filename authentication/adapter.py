from google.auth.transport import requests
from google.oauth2 import id_token
from django.contrib.auth import authenticate
from users.models import User, ClientUser
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from annotation.models import Client
from users.models import ClientUser
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

User = get_user_model()


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())

            if "accounts.google.com" in id_info["iss"]:
                return id_info

        except:
            return "The Token is either invalid or Expired"


def register_client_user(user_data):
    email = user_data.get("email")
    user_domain = user_data.get("user_domain")
    client = Client.objects.get(domain_name=user_domain)
    try:
        user = User.objects.get(email=email)
        client_user = ClientUser.objects.get(user=user)
    except User.DoesNotExist:
        user = User.objects.create(user_type="client", email=email)
        client_user = ClientUser.objects.get(user=user)
        client_user.client = client
        client_user.save()
    user = authenticate(username=email)
    if not user:
        return None
    return {
        "data": {
            "user": {
                "full_name": user.get_full_name(),
                "email": user.email,
            },
            "client": {"name": client.name, "domain_name": client.domain_name},
            "is_admin": client_user.is_admin,
            "token":User.token(user)
        }
    }
