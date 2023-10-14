from django.test import TestCase

from rest_framework import serializers

from annotation.serializers import StepSerializer, StepSubmitSerializer, TaskResetSerializer
from users.tests.factories import UserFactory
from annotation.tests.factories import UrlFactory, TaskFactory


class StepSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(email='miracle@gmail.com')
        self.task = TaskFactory()

    def test_step_serializer(self):
        '''Test step serializer'''

        step_data = {
            'task': self.task,
            'step': 'products_entities',
            'step_data': {'data': 'data'},
            'count': 2,
            'url': 'centricityinsights.com',
            'archived_url': 'google.com',
        }
        step = StepSerializer(data=step_data)

        self.assertTrue(step.is_valid())


class StepSubmitSerializerTest(TestCase):

    def setUp(self):
        self.data = {
        'url': 'centricityinsights.com',
        'step_data': {'data': 'data'},
        'step': 'page_products'
        }

    def test_url_validity(self):
        '''Assert that serializer raises url validity error duely'''

        sss = StepSubmitSerializer(data=self.data)

        self.assertRaises(serializers.ValidationError)
        self.assertFalse(sss.is_valid())

    def test_step_submit(self):

        # Add the url to URL model
        UrlFactory(url=self.data['url']) 
        sss = StepSubmitSerializer(data=self.data)

        self.assertTrue(sss.is_valid())        


class TaskResetSerializerTest(TestCase):

    def test_url_validity(self):
        '''Test that the serializer functions properly'''
        
        data = {
            'url': 'centricityinsights.com'
        }
        trs = TaskResetSerializer(data=data)

        self.assertRaises(serializers.ValidationError)
        self.assertFalse(trs.is_valid())

        UrlFactory(url=data['url'])
        trs = TaskResetSerializer(data=data)

        self.assertTrue(trs.is_valid())