from django.test import TestCase

from users.tests.factories import UserFactory
from annotation.tests.factories import UrlFactory, TaskFactory, StepFactory, DomainPriorityFactory


class DomainPriorityTest(TestCase):

    def test_model_creation(self):
        '''Assert that the domain priority model was with correct defaults'''

        domain = DomainPriorityFactory()

        self.assertIsNotNone(domain.domain) 
        self.assertIsNotNone(domain.approximate_urls) 
        self.assertIsNotNone(domain.views) 
        self.assertIsNotNone(domain.last_counted) 
        self.assertIsNotNone(domain.status) 


class UrlTesT(TestCase):

    def test_model_creation(self):
        '''Assert that the url model was with correct defaults'''

        url = UrlFactory()

        self.assertIsNotNone(url.url) 
        self.assertIsNotNone(url.page_views) 
        self.assertIsNotNone(url.known) 
        self.assertIsNotNone(url.events) 
        self.assertIsNotNone(url.archived_url) 

    def test_queued(self):
        '''Assert that the queued property works'''
    
        url = UrlFactory(status='green', known=False)

        self.assertTrue(url.queued)


class TaskTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_model_creation(self):

        url = UrlFactory()
        task = TaskFactory(user=self.user, url=url)
    
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.url, url)
     

class StepTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        url = UrlFactory()
        self.task = TaskFactory(url=url, user=self.user)

    def test_model_creation(self):
        step_data = {
            'task': self.task,
            'step': 'products_entities',
            'step_data': {'data': 'data'}
        }
        step = StepFactory(**step_data)

        self.assertEqual(step.task, step_data['task'])
        self.assertEqual(step.step, step_data['step'])
        self.assertEqual(step.step_data, step_data['step_data'])
