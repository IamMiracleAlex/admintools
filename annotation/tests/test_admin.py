from django.test import TestCase
from django.urls import reverse

from users.tests.factories import UserFactory
from annotation.tests import factories


class TaskAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.task = factories.TaskFactory() 

    def test_changelist_view(self):
        '''Test Task change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.task._meta.app_label, self.task._meta.model_name))
        page = self.client.get(url)
        # Assert page loads
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test Task change view page'''

        url = reverse("admin:%s_%s_change" % (self.task._meta.app_label, self.task._meta.model_name), args=(self.task.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
    

class UrlAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.url = factories.UrlFactory() 

    def test_changelist_view(self):
        '''Test url change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.url._meta.app_label, self.url._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test url change view page'''

        url = reverse("admin:%s_%s_change" % (self.url._meta.app_label, self.url._meta.model_name), args=(self.url.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class RawUrlAdminTest(TestCase):    

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.raw_url = factories.RawUrlFactory() 

    def test_changelist_view(self):
        '''Test raw url change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.raw_url._meta.app_label, self.raw_url._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test raw url change view page'''

        url = reverse("admin:%s_%s_change" % (self.raw_url._meta.app_label, self.raw_url._meta.model_name), args=(self.raw_url.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class DomainPriorityAdminTest(TestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.domain = factories.DomainPriorityFactory() 

    def test_changelist_view(self):
        '''Test domain change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.domain._meta.app_label, self.domain._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test domain change view page'''

        url = reverse("admin:%s_%s_change" % (self.domain._meta.app_label, self.domain._meta.model_name), args=(self.domain.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200) 


class IntentDataAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.intent = factories.IntentDataFactory() 

    def test_changelist_view(self):
        '''Test intent data change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.intent._meta.app_label, self.intent._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test intent data change view page'''

        url = reverse("admin:%s_%s_change" % (self.intent._meta.app_label, self.intent._meta.model_name), args=(self.intent.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)     


class KnownUrlsAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.known_urls = factories.KnownUrlFactory() 

    def test_changelist_view(self):
        '''Test intent data change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.known_urls._meta.app_label, self.known_urls._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test intent data change view page'''

        url = reverse("admin:%s_%s_change" % (self.known_urls._meta.app_label, self.known_urls._meta.model_name), args=(self.known_urls.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   


class TBAQAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.tbaq = factories.TBAQFactory() 

    def test_changelist_view(self):
        '''Test tbaq change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.tbaq._meta.app_label, self.tbaq._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test tbaq change view page'''

        url = reverse("admin:%s_%s_change" % (self.tbaq._meta.app_label, self.tbaq._meta.model_name), args=(self.tbaq.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   
    

class ArchiveQueueTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.arhive_queue = factories.ArchiveQueueFactory() 

    def test_changelist_view(self):
        '''Test arhive_queue change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.arhive_queue._meta.app_label, self.arhive_queue._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test arhive_queue change view page'''

        url = reverse("admin:%s_%s_change" % (self.arhive_queue._meta.app_label, self.arhive_queue._meta.model_name), args=(self.arhive_queue.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class CountryAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.country = factories.CountryFactory() 

    def test_changelist_view(self):
        '''Test Country change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.country._meta.app_label, self.country._meta.model_name))
        page = self.client.get(url)
        # Assert page loads
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test country change view page'''

        url = reverse("admin:%s_%s_change" % (self.country._meta.app_label, self.country._meta.model_name), args=(self.country.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class ClientAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.client_ = factories.ClientFactory() 

    def test_changelist_view(self):
        '''Test client change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.client_._meta.app_label, self.client_._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test client change view page'''

        url = reverse("admin:%s_%s_change" % (self.client_._meta.app_label, self.client_._meta.model_name), args=(self.client_.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

        
class QueueUrlRelationshipAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.queue = factories.QueueUrlRelationshipFactory() 

    def test_changelist_view(self):
        '''Test queue change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.queue._meta.app_label, self.queue._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test queue change view page'''

        url = reverse("admin:%s_%s_change" % (self.queue._meta.app_label, self.queue._meta.model_name), args=(self.queue.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        
        
class BeeswaxListAdmin(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.beeswax = factories.BeeswaxListFactory() 

    def test_changelist_view(self):
        '''Test beeswax change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.beeswax._meta.app_label, self.beeswax._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test beeswax change view page'''

        url = reverse("admin:%s_%s_change" % (self.beeswax._meta.app_label, self.beeswax._meta.model_name), args=(self.beeswax.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class ClientDomainRelationshipAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.domain = factories.ClientDomainRelationshipFactory() 

    def test_changelist_view(self):
        '''Test client domain  change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.domain._meta.app_label, self.domain._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test client domain change view page'''

        url = reverse("admin:%s_%s_change" % (self.domain._meta.app_label, self.domain._meta.model_name), args=(self.domain.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class FacetPropertyAdminAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.facet = factories.FacetPropertyFactory() 

    def test_changelist_view(self):
        '''Test facet change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.facet._meta.app_label, self.facet._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)

    def test_change_view(self):
        '''Test facet change view page'''

        url = reverse("admin:%s_%s_change" % (self.facet._meta.app_label, self.facet._meta.model_name), args=(self.facet.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class UrlEditorAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.urleditor = factories.UrlEditorFactory() 

    def test_changelist_view(self):
        '''Test url editor change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.urleditor._meta.app_label, self.urleditor._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)


class UrlScrapedAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.url_scrapped = factories.UrlScrapedFactory() 

    def test_changelist_view(self):
        '''Test url scrapped change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.url_scrapped._meta.app_label, self.url_scrapped._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        
    def test_change_view(self):
        '''Test url scrapped change view page'''

        url = reverse("admin:%s_%s_change" % (self.url_scrapped._meta.app_label, self.url_scrapped._meta.model_name), args=(self.url_scrapped.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   


class ExtensionVersionAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.ce_version = factories.ExtensionVersionFactory() 

    def test_changelist_view(self):
        '''Test ce version change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.ce_version._meta.app_label, self.ce_version._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        
    def test_change_view(self):
        '''Test ce version change view page'''

        url = reverse("admin:%s_%s_change" % (self.ce_version._meta.app_label, self.ce_version._meta.model_name), args=(self.ce_version.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)  


class TaskBreakdownAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.task = factories.TaskBreakdownFactory() 

    def test_changelist_view(self):
        '''Test task breakdown change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.task._meta.app_label, self.task._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)
        
    def test_change_view(self):
        '''Test task breakdown change view page'''

        url = reverse("admin:%s_%s_change" % (self.task._meta.app_label, self.task._meta.model_name), args=(self.task.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)    


class DomainLogAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        self.domain_log = factories.DomainLogFactory() 

    def test_changelist_view(self):
        '''Test domain log change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.domain_log._meta.app_label, self.domain_log._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   


class NewTBAQAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user) 
        url = factories.UrlFactory(status="green")
        self.newtbaq = factories.NewTBAQFactory(url=url) 

    def test_changelist_view(self):
        '''Test new tbaq change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.newtbaq._meta.app_label, self.newtbaq._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   

    def test_change_view(self):
        '''Test new tbaq change view page'''

        url = reverse("admin:%s_%s_change" % (self.newtbaq._meta.app_label, self.newtbaq._meta.model_name), args=(self.newtbaq.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   


class BadUrlsAdminTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user)
        self.url = factories.UrlFactory() 
        self.bad_url = factories.TaskFactory(url=self.url, user=self.user) # create a bad task
        # create a corresponding step
        factories.StepFactory(task=self.bad_url, step="bad_url")

    def test_changelist_view(self):
        '''Test bad urls change list view'''

        url = reverse("admin:%s_%s_changelist" % (self.bad_url._meta.app_label, self.bad_url._meta.model_name))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)   

    def test_change_view(self):
        '''Test bad urls change view page'''

        url = reverse("admin:%s_%s_change" % (self.bad_url._meta.app_label, self.bad_url._meta.model_name), args=(self.bad_url.pk,))
        # url = reverse("admin:annotation_badurl_change", args=(self.bad_urls.pk,))
        page = self.client.get(url)
        self.assertEqual(page.status_code, 200)    