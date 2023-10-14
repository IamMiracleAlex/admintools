from django.test import TestCase
from classification.tests.factories import FacetValueFactory, NodeFactory


class NodeTest(TestCase):
    
    def test_all_new_nodes_facet_carrying_sometimes(self):
        """
        A new node should inherit all parental facet property, 
        or carry all existing facet properties as `sometimes` if it is a departmental node.
        """
        
        # populate facets
        FacetValueFactory.create_batch(size=30)
       
        node1 = NodeFactory()
        node2 = NodeFactory(parent=node1)
        node3 = NodeFactory(parent=node2)
        
        # assertions
        self.assertEqual(node3.facet_properties.last().has_facet, "never")
        self.assertEqual(node2.facet_properties.last().has_facet, "never")


       