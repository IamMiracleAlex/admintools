from rest_framework.test import APITestCase
from rest_framework import status

from classification.models import NodeFacetRelationship
from users.tests.factories import UserFactory
from classification.tests.factories import FacetCategoryFactory, FacetValueFactory, NodeFactory


class FacetCategoryTests(APITestCase):
    """
    Tests for the Facet Category in the classification app
    """

    def setUp(self):
        self.url = "/classification/facet_category/"
        self.user = UserFactory(is_superuser=True)  
        self.data = [{
                "title": "FEMALE CLOTHING",
                "description": "This is for the men line"
            },{
                "title": "MALE CLOTHING",
                "description": "This is for the men line"
            }]

    def test_create_facet_category(self):
        """
            Ensure that we can create a new facet category
        """

        self.client.force_authenticate(self.user)
        response1 = self.client.post(self.url, self.data[0], format="json")
        response2 = self.client.post(self.url, self.data[1], format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)


    def test_delete_facet_category(self):
        """
            Ensure that we can delete a facet category
        """        
        self.client.force_authenticate(self.user)
        facet_cat_lists = FacetCategoryFactory.create_batch(size=2)
        response = self.client.delete("{}{}/".format(self.url, facet_cat_lists[0].id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_facet_category(self):
        """
            Ensure that the facet category is successfully updated
        """    
        self.client.force_authenticate(self.user)
        
        obj = FacetCategoryFactory()
        resp = self.client.patch("{}{}/".format(self.url, obj.id), {"title": "ANOTHER TITLE"}, format="json")   
        self.assertEqual(resp.status_code, status.HTTP_200_OK) 
        self.assertEqual(resp.json()['title'], "ANOTHER TITLE")


class FacetValueTest(APITestCase):
    """
        Test for the Facet Value in classification app
    """
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        cat = FacetCategoryFactory()
        self.data = [
            {
                "category": cat.id,
                "label": "another facet",
                "description": "facet description"
            },
            {
                "category": cat.id,
                "label": "facet 2",
                "description": "facet description 2"
            }
        ]
        self.url = "/classification/facet/"
    
    def test_create_new_facet(self):
        """
            Ensure that we can create a Facet Value
        """
        self.client.force_authenticate(self.user)
        resp = self.client.post(self.url, self.data[0], format="json")

        # assert that it returns a 201 status code
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json()['label'], self.data[0]['label'])

    def test_delete_facet(self):
        """
            Ensure that a single facet is delete by passing its id
        """
        self.client.force_authenticate(self.user)
        facets =  FacetValueFactory.create_batch(size=2)
        response = self.client.delete('{}{}/'.format(self.url, facets[0].id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # CASE 2
        '''Return 404_NOT_FOUND error when an incorrect id is passed'''
        response2 = self.client.delete('{}{}/'.format(self.url, 1))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

       

class NodeTest(APITestCase):
    """
        Test cases for modules in the Node model
    """
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.url = "/classification/nodes/"
        self.data = [
            {
                "title": "BIN",
                "description": "first",
                "parent": None,
                "facet_properties": []
            },
            {
                "title": "FEMALE CLOTHING",
                "description": "This is for the men line",
                "parent": None,
                 "facet_properties": [] 
            }

        ]
    
    def test_create_node(self):
        """
            Create a new node
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data[0], format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_all_nodes(self):
        """
            Return all nodes in the db
        """
        self.client.force_authenticate(self.user)
        nodes = NodeFactory.create_batch(size=4)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(nodes), len(resp.data))
    
    def test_get_single_node(self):
        """
            Returning a single node and all its children in the db
        """
        self.client.force_authenticate(self.user)
        node = NodeFactory()
        # Retrieve a single node now
        resp = self.client.get("{}{}/treeview/".format(self.url, node.id))

        self.assertEqual(resp.json()['title'], node.title)


    def test_delete_single_node(self):
        """
            Test deleting of single nodes
        """
        node = NodeFactory()
        self.client.force_authenticate(self.user)
        # Delete single node
        resp = self.client.delete("{}{}/".format(self.url, node.id))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


    def test_bulk_updating_facets_and_facet_inheritance(self):
        """
            Bulk assign facets
        """
        self.client.force_authenticate(self.user)

        # Create a list of nodes
        node0 = NodeFactory()
        node1 = NodeFactory(parent=node0)
        node2 = NodeFactory(parent=node1)

        # Create facets
        cat = FacetCategoryFactory()
        facets = FacetValueFactory.create_batch(size=2, category=cat)
        
        # get the node facet relationships
        n1_facet_relationship = NodeFacetRelationship.objects.filter(node=node0)
        n3_facet_relationship = NodeFacetRelationship.objects.filter(node=node2)
        
        self.assertTrue(all([n1_facet_relationship, n3_facet_relationship]))

    def test_all_new_nodes_facet_carrying_sometimes(self):
        """
        Assert that all new nodes should inherit 
        parent facets and carries sometimes as facet value
        """
        self.client.force_authenticate(self.user)

        # Create facets
        FacetValueFactory.create_batch(size=4)    

        # create nodes
        node0 = NodeFactory()
        node1 = NodeFactory(parent=node0)
        node2 = NodeFactory(parent=node1)

        # assert that all nodes have same facets with their parents defaulting to 'sometimes'
        self.assertEqual(node0.facet_properties.all()[0].has_facet, "never")
        self.assertEqual(node1.facet_properties.all()[0].has_facet, "never")
        self.assertEqual(node2.facet_properties.all()[0].has_facet, "never")

    def test_facet_for_ce(self):
        self.client.force_authenticate(self.user)
        facets = FacetValueFactory.create_batch(size=20)
        node = NodeFactory(facets=facets)
        #Default value is "never".  but for this test, we need them to be "sometimes"
        node.facet_properties.all().update(has_facet="sometimes")
        version_url = '{}{}/facets_for_ce/?version=1.10.1'.format(self.url, node.id)

        # CASE 1: Test with version appended
        res = self.client.get(version_url)
        intended_version_res = {
                "facets": [
                {
                    "id": facets[0].id,
                    "category": facets[0].category.title,
                    "label": facets[0].label,
                    "description": facets[0].description,
                    "has_facet": "sometimes"
                }
                ],
                "facet_category": facets[0].category.title,
                "category_type": facets[0].category.facet_type,
            }
        assumed_res = res.json()[0]
        self.assertEqual(node.facet_properties.count(), 20)
        self.assertEqual(assumed_res['facets'][0],intended_version_res['facets'][0])

        # CASE 2: Test without version appended
        versionless_url = version_url.split('?')[0]
        versionless_res = self.client.get(versionless_url)
        intended = {
                    "id": facets[0].id,
                    "category": facets[0].category.title,
                    "label": facets[0].label,
                    "description": facets[0].description,
                    "has_facet": "sometimes"
                },
        assumed = versionless_res.json()
        self.assertEqual(assumed[0], intended[0])
