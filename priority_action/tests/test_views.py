import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import ClientUser
from priority_action.models import (
    Intent,
    IntentChange,
    Correlation,
    CorrelationChange,
    Sales,
    SalesChange,
)
from annotation.models import Client


def create_user():
    user_data = {
        "email": "dwight.schrute@schrutefarms.centricity.cloud",
        "first_name": "Dwight",
        "last_name": "Schrute",
        "is_staff": False,
        "user_type": "client",
    }

    user = get_user_model().objects.create_user(**user_data)
    client_user = ClientUser.objects.get(user=user)
    client = Client.objects.first()
    client_user.client = client
    client_user.is_admin = True
    client_user.save()
    return user


def create_client():
    client_data = {"name": "Schrute Farms"}
    return Client.objects.create(**client_data)


class IntentTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/intent/"
        self.intent_data = {"organization": self.organization}

    def test_get_intent_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_intent_action(self):
        intent = Intent.objects.create(organization=self.organization)
        data = {
            "value": 1,
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class IntentChangeTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/intent_change/"

    def test_get_intent_change_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_intent_change_action(self):
        IntentChange.objects.create(organization=self.organization)
        data = {
            "value": "0.21",
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class CorrelationTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/correlation/"

    def test_get_correlation_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_correlation_action(self):
        Correlation.objects.create(organization=self.organization)
        data = {
            "value": "0.5",
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class CorrelationChangeTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/correlation_change/"

    def test_get_correlation_change_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_correlation_change_action(self):
        CorrelationChange.objects.create(organization=self.organization)
        data = {
            "value": "0.20",
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class SalesTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/sales/"

    def test_get_sales_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_sales_action(self):
        Sales.objects.create(organization=self.organization)
        data = {
            "value": 1,
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class SalesChangeTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/sales_change/"

    def test_get_sales_change_action(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_update_sales_change_action(self):
        SalesChange.objects.create(organization=self.organization)
        data = {
            "value": "0.03",
            "value_operator": "=",
            "period_operator": "sum",
            "status": True,
            "organization": self.organization.id,
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(
            self.url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)


class PeriodTest(APITestCase):
    def setUp(self):
        self.organization = create_client()
        self.user = create_user()
        self.url = "/api/priority_action/periods/"
