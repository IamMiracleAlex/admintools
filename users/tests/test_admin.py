from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory


class TaxonomyEditorAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 

    def test_changelist_view(self):
        '''Test user change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.user._meta.app_label, self.user._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test user change view page'''

        url = reverse("admin:%s_%s_change" % (self.user._meta.app_label, self.user._meta.model_name), args=(self.user.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)