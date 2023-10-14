from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory
from classification.tests import factories


class TaxonomyEditorAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.taxeditor = factories.TaxonomyEditorFactory() 

    def test_changelist_view(self):
        '''Test Taxonomy editor change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.taxeditor._meta.app_label, self.taxeditor._meta.model_name))
        page = self.client.get(url)
        # Assert page loads
        self.assertEqual(page.status_code, 200)


class FacetCategoryAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.facetcat = factories.FacetCategoryFactory() 

    def test_changelist_view(self):
        '''Test facet category change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.facetcat._meta.app_label, self.facetcat._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test facet category change view page'''

        url = reverse("admin:%s_%s_change" % (self.facetcat._meta.app_label, self.facetcat._meta.model_name), args=(self.facetcat.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class FacetValueAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.facetval = factories.FacetValueFactory() 

    def test_changelist_view(self):
        '''Test facet value change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.facetval._meta.app_label, self.facetval._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test facet value change view page'''

        url = reverse("admin:%s_%s_change" % (self.facetval._meta.app_label, self.facetval._meta.model_name), args=(self.facetval.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

class NodeFacetRelationshipAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.node_relation = factories.NodeFacetRelationshipFactory( has_facet="sometimes") 

    def test_changelist_view(self):
        '''Test node facet relationship change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.node_relation._meta.app_label, self.node_relation._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test node facet relationship change view page'''

        url = reverse("admin:%s_%s_change" % (self.node_relation._meta.app_label, self.node_relation._meta.model_name), args=(self.node_relation.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class NodeAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.node = factories.NodeFactory(status='active') 

    def test_changelist_view(self):
        '''Test node change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.node._meta.app_label, self.node._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test node change view page'''

        url = reverse("admin:%s_%s_change" % (self.node._meta.app_label, self.node._meta.model_name), args=(self.node.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class DeletedNodeAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.deleted_node = factories.DeletedNodeFactory(status='deleted') 

    def test_changelist_view(self):
        '''Test deleted node change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.deleted_node._meta.app_label, self.deleted_node._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test deleted node change view page'''

        url = reverse("admin:%s_%s_change" % (self.deleted_node._meta.app_label, self.deleted_node._meta.model_name), args=(self.deleted_node.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)    