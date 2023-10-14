from rest_framework.test import APITestCase
from classification.utils import is_allowed
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class UserPermissionTest(APITestCase):
    """
    Tests for the Facet Category in the classification app
    """

    def setUp(self):
        # self.client = APIClient()    
        self.url = "/classification/facet_category/"
        User = get_user_model()
        self.user = User.objects.create_superuser("test@test.com", "test1234")
        self.group1 = Group.objects.get_or_create(name='taxonomy')
        self.group2 = Group.objects.get_or_create(name='taxonomy-annotator')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
    
    def test_user_is_not_allowed(self):
        self.assertFalse(is_allowed(self.user, group_names=['taxonomy',]))
    
    def test_user_allowed(self):
       user = get_user_model().objects.create_user("test2@test.com", "test1234")
       group1 = Group.objects.get(name='taxonomy')
       group1.user_set.add(user)
       
       self.assertTrue(is_allowed(user, group_names=['taxonomy']))
    
    def test_for_403_response_for_superusers(self):
        user = get_user_model().objects.create_user("test2@test.com", "test1234")
        token = Token.objects.create(user=user)
        token.save()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = "/classification/nodes/"
        data = {
                "title": "NODE 1", 
                "description": "", 
                "parent": None, 
                "facet_properties": []
            }
        res = client.post(url, data,  format="json")
        
        self.assertEqual(res.status_code, 403)





