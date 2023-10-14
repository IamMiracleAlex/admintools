from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory
from custom_admin.tests import factories


class BulkEditAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.bulkedit = factories.BulkEditFactory()

    def test_changelist_view(self):
        '''Test bulk edit list view'''

        url = reverse("admin:%s_%s_changelist" % (self.bulkedit._meta.app_label, self.bulkedit._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)