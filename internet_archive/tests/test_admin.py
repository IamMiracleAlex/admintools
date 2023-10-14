from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory
from internet_archive.tests import factories


class ArchiveSettingAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.archive = factories.ArchiveSettingFactory()

    def test_changelist_view(self):
        '''Test archive setting list view'''

        url = reverse("admin:%s_%s_changelist" % (self.archive._meta.app_label, self.archive._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test archive setting change view page'''

        url = reverse("admin:%s_%s_change" % (self.archive._meta.app_label, self.archive._meta.model_name), args=(self.archive.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)