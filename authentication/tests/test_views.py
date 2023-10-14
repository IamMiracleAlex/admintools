import json
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import ClientUser
from django.contrib.auth import get_user_model
from annotation.models import Client
from unittest.mock import patch
from django.conf import settings
from django.test.utils import override_settings

User = get_user_model()


def create_user():
    user_data = {
        "email": "dwight.schrute@schrutefarms.centricity.cloud",
        "first_name": "Dwight",
        "last_name": "Schrute",
        "is_staff": False,
        "user_type": "client",
    }
    user = User.objects.create(**user_data)
    client_user = ClientUser.objects.get(user=user)
    client = Client.objects.first()
    client_user.client = client
    client_user.is_admin = True
    client_user.save()
    return user


def create_client():
    client_data = {"name": "Schrute Farms", "domain_name":"schrutefarms.centricity.cloud"}
    return Client.objects.create(**client_data)

def mocked_verify_oauth2_token(*args,  **kwargs):
    return {
        "iss":["accounts.google.com"],
        "aud":settings.GOOGLE_CLIENT_ID,
        "email": "dwight.schrute@schrutefarms.centricity.cloud",
    }
def false_mocked_verify_oauth2_token(*args, **kwargs):
    return {
        "iss":["accounts.google.com"],
        "aud":settings.GOOGLE_CLIENT_ID,
        "email": "unknown@invalid.false.wrong",
    }

def mocked_get_current_site(*args, domain=None, **kwargs):
    class MockResponse:
        @property
        def domain(self):
            return domain or "schrutefarms.centricity.cloud"
    return MockResponse()


class GoogleAuthViewTest(APITestCase):
    def setUp(self):
        self.url = "/api/authentication/login/"
        self.organization = create_client()
        self.user = create_user()
        
    @patch("authentication.adapter.id_token.verify_oauth2_token", side_effect=mocked_verify_oauth2_token)
    def test_signin(self, mocked_oauth):
        data = {
            "auth_token":"randomstrings"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.json(), dict)

    @patch("authentication.adapter.id_token.verify_oauth2_token", side_effect=false_mocked_verify_oauth2_token)
    def test_invalid_user_domain(self, mocked_oauth):
        data = {
            "auth_token":"randomstrings"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response.json(), dict)
