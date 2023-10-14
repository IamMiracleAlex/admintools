from django.test import TestCase
from django.urls import reverse

from custom_logger.tests import factories
from users.tests.factories import UserFactory


class RequestLogAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.request_log = factories.RequestLogFactory()

    def test_changelist_view(self):
        '''Test request log list view'''

        url = reverse("admin:%s_%s_changelist" % (self.request_log._meta.app_label, self.request_log._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test request log change view page'''

        url = reverse("admin:%s_%s_change" % (self.request_log._meta.app_label, self.request_log._meta.model_name), args=(self.request_log.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class ChromeExtensionLogAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.celog = factories.ChromeExtensionLogFactory()

    def test_changelist_view(self):
        '''Test ce log list view'''

        url = reverse("admin:%s_%s_changelist" % (self.celog._meta.app_label, self.celog._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test ce log change view page'''

        url = reverse("admin:%s_%s_change" % (self.celog._meta.app_label, self.celog._meta.model_name), args=(self.celog.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)