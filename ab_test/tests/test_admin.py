from django.test import TestCase
from django.urls import reverse

from ab_test.tests import factories
from users.tests.factories import UserFactory


class TestSetupAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.test_setup = factories.TestSetupFactory()

    def test_changelist_view(self):
        '''Test test setup list view'''

        url = reverse("admin:%s_%s_changelist" % (self.test_setup._meta.app_label, self.test_setup._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class TestInProgressAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.test_progress = factories.TestInProgressFactory()

    def test_changelist_view(self):
        '''Test request log list view'''

        url = reverse("admin:%s_%s_changelist" % (self.test_progress._meta.app_label, self.test_progress._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class TestResultAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.test_reult = factories.TestResultFactory()

    def test_changelist_view(self):
        '''Test test results list view'''

        url = reverse("admin:%s_%s_changelist" % (self.test_reult._meta.app_label, self.test_reult._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
