from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory
from admintool.tests import factories


class StatusAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.status = factories.StatusFactory()

    def test_changelist_view(self):
        '''Test status list view'''

        url = reverse("admin:%s_%s_changelist" % (self.status._meta.app_label, self.status._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)



class DataStatusAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.data_status = factories.DataStatusFactory()

    def test_changelist_view(self):
        '''Test data status list view'''

        url = reverse("admin:%s_%s_changelist" % (self.data_status._meta.app_label, self.data_status._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test data status change view page'''

        url = reverse("admin:%s_%s_change" % (self.data_status._meta.app_label, self.data_status._meta.model_name), args=(self.data_status.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)