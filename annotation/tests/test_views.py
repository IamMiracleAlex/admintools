from rest_framework.test import APITestCase
from rest_framework import status

from annotation.views import AnnotationHandler
from annotation.models import Task
from annotation.tests.factories import (UrlFactory, TaskFactory, StepFactory,
    ClientFactory, CountryFactory)
from users.tests.factories import UserFactory
from classification.tests.factories import FacetValueFactory, NodeFactory


class AnnotationHandlerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.url_obj = UrlFactory(url='https://centricityinsights.com', 
                                    known=False, 
                                    status="green")
        self.url = '/annotation/'

    def test_get(self):
        '''Assert that GET method fetches a url from annotation queue and creates
            a new task from it or retrieve an existing incomplete task 
        '''

        '''
        CASE 1:
            Assert that endpoint creates a new task if old task does not exist
        '''
        data = {'mode': 'annotator'}
        self.client.force_authenticate(self.user)     
        resp = self.client.get(self.url, data=data)
        task = Task.objects.get(url=self.url_obj)

        # confirm creation
        self.assertEqual(task.url.url, self.url_obj.url)

        '''
        CASE 2:
            Assert that the endpoints retrieves an exisiting task when it exists
            and do not create a new one
        '''

        self.client.get(self.url, data=data)
        count = Task.objects.count()

        self.assertEqual(count, 1)

        # check returned data
        self.assertEqual(self.url_obj.url, resp.data['url'])
        self.assertEqual(self.url_obj.archived_url, resp.data['archived_url'])
        self.assertEqual(self.user.email, resp.data['Attributes']['step-user'])

    def test_post(self):
        '''A new step is returned after each submission or a new task if the last
        step was submitted'''
        
        '''CASE 1:
            When no tasks is available
        '''
        # request data
        data = {
            'url': 'https://centricityinsights.com',
            'step_data': {'data': 'sample data'},
            'step': 'page_products'
        }
        # authenticate user and make request
        self.client.force_authenticate(self.user)   
        resp = self.client.post(self.url, data=data, format='json')
        
        # error message is given
        self.assertEqual(resp.data['detail'], 'Task not found')

        '''CASE 2:
            Assert that a new step is returned after each submission
        '''

        task = TaskFactory(user=self.user, url=self.url_obj)
        StepFactory(task=task)
        resp = self.client.post(self.url, data=data, format='json')

        # new step is returned (2nd step)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['step'], 'products_entities')

        '''CASE 3:
            Assert that the last step is returned 
        '''
        # update request data
        data['step'] = 'products_entities'
        resp = self.client.post(self.url, data=data, format='json')

        # new step is returned (3rd step)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['step'], 'entities_classification')
       
        '''CASE 4:
            Assert that a new task is returned after last submission
        '''
        # update request data to contain the last valid step and necessary data
        nodes = NodeFactory.create_batch(3)
        factes = FacetValueFactory.create_batch(3)
       
        data.update(
            {   
                "step": "entities_classification",
                "product_ids": [1,2,3],
                "names": ["mode","myth", "cors"],
                "xpaths": ["/HTML[1]/BODY[1]/MAIN[1]", "/HTML[1]/BODY[1]/MAIN[1]", "/HTML[1]/BODY[1]/MAIN[1]"],
                "intents": [1, 2,3],
                "node_ids": [node.id for node in nodes],
                "facet_ids": [facet.id for facet in factes],
                "has_facets": ["yes", "no", "yes"]
            }
        )
        self.second_url_obj = UrlFactory(url='www.netflix.com', known=False, status="green")
        resp = self.client.post(self.url, data=data, format='json')

        # Assert new task is created with new url
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['url'], self.second_url_obj.url)
        self.assertEqual(resp.data['step'], 'page_products') # has the first step

        '''CASE 5:
            Assert that when current step is `bad_url`, a new task is created with
            fresh step.
        '''  
        # update data to have `step` as 'bad_url` 
        data['step_data']["badUrlState"] = 'bad_url' 
        resp = self.client.post(self.url, data=data, format='json')

        # new task with the first step
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['step'], 'page_products') 


class UrlsListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url_obj = UrlFactory() 
        
    def test_list_urls(self):
        '''Assert urls are listed'''

        url = '/annotation/all-urls/'
        # authenticate user and make request
        self.client.force_authenticate(self.user)   
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    
    def test_search_urls(self):
        '''Assert that url search works as expected'''

        url = "/annotation/all-urls/?q=https://centricityinsights.com/"
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
    def test_filter_urls(self):
        '''Assert that filter works as expected'''

        url = f"/annotation/all-urls/?status={self.url_obj.status}"
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class UrlsCreateViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_url_create(self):
        '''Assert that url create endpoint works'''

        country = CountryFactory()
        data = {
            'url': 'https://google.com/how-to-cook-beans/',
            'page_views': 1,
            'priority': 1,
            'status': 'green',
            'countries': [country.id]
        }
        url = '/annotation/add-url/'
        self.client.force_authenticate(self.user)
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class ClientsCountriesListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
      
    def test_countries_list(self):
        '''Assert that countries lists are returned'''

        country = CountryFactory()
        url = '/annotation/countries/'
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data[0]['name'], country.name)
        

    def test_clients_list(self):
        '''Assert that clients are returned'''

        client = ClientFactory()
        url = '/annotation/clients/'
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data[0]['name'], client.name)


class UrlRetrieveViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_retrieve_url(self):
        '''Assert that url is retrieved'''

        obj = UrlFactory()
        url = f'/annotation/urls/{obj.id}/'
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['url'], obj.url)


class UrlUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_update(self):
        '''Assert that update works'''

        client = ClientFactory()
        obj = UrlFactory()
        data = {"url": obj.id,
            "status": "green",
            "priority": 3,
            "clients": [client.id,],
        }
        url = f'/annotation/urls/edit/'
        self.client.force_authenticate(self.user)
        resp = self.client.post(url, data=data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, 'Urls updated successfully')


class UrlDeleteResetViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_delete(self):
        '''Assert that deleting a url works'''

        obj = UrlFactory()
        data = {
            'url_ids': [obj.id,]
        }
        url = '/annotation/urls/delete/'
        self.client.force_authenticate(self.user)
        resp = self.client.delete(url, data=data, format='json')
        
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('urls deleted successfully', resp.data)
