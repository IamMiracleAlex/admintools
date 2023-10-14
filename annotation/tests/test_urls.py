from django.test import SimpleTestCase
from django.urls import resolve

from annotation import views



class AnnotationUrlTests(SimpleTestCase):

    def test_annotation_handler_resolves_to_view(self):
        '''Assert that annotation_handler resolves to view'''

        # resolves to the func.view_class
        found = resolve('/annotation/')
        self.assertEquals(found.func.view_class, views.AnnotationHandler)

    def test_ce_download_resolves_to_view(self):
        '''Assert that ce_download url resolves to view'''

        found = resolve('/annotation/download-extension/')
        self.assertEquals(found.func.view_class, views.CEDownloadView)

    def test_reset_tasks_resolves_to_view(self):
        '''Assert that reset_tasks resolves to view'''

        found = resolve('/annotation/reset-task/')
        self.assertEquals(found.func.view_class, views.ResetTask)

    def test_tbaq_count_resolves_to_view(self):
        '''Assert that tbaq_count resolves to view'''

        found = resolve('/annotation/tbaq-count/')
        self.assertEquals(found.func.view_class, views.TBAQCount)


class URLEditorUrlTests(SimpleTestCase):

    def test_all_urls_resolves_to_view(self):
        '''Assert that UrlList resolves to view'''

        # resolves to the func.view_class
        found = resolve('/annotation/all-urls/')
        self.assertEquals(found.func.view_class, views.UrlsListView)

    def test_add_url_resolves_to_view(self):
        '''Assert that UrlsCreate resolves to view'''

        found = resolve('/annotation/add-url/')
        self.assertEquals(found.func.view_class, views.UrlsCreateView)

    def test_retrieve_urls_resolves_to_view(self):
        '''Assert that UrlRetrieve resolves to view'''

        found = resolve('/annotation/urls/1/')
        self.assertEquals(found.func.view_class, views.UrlRetrieveView)

    def test_delete_urls_resolves_to_view(self):
        '''Assert that UrlDelete resolves to view'''

        found = resolve('/annotation/urls/delete/')
        self.assertEquals(found.func.view_class, views.UrlDeleteResetView)

    def test_edit_urls_resolves_to_view(self):
        '''Assert that UrlUpdate resolves to view'''

        found = resolve('/annotation/urls/edit/')
        self.assertEquals(found.func.view_class, views.UrlUpdateView)

    def test_urls_reset_resolves_to_view(self):
        '''Assert that UrlReset resolves to view'''

        found = resolve('/annotation/urls/reset/')
        self.assertEquals(found.func.view_class, views.UrlDeleteResetView)

    def test_assigned_urls_resolves_to_view(self):
        '''Assert that ListAssignedUrls resolves to view'''

        found = resolve('/annotation/assigned-urls/')
        self.assertEquals(found.func.view_class, views.ListAssignedUrlsView)


    def test_clients_resolves_to_view(self):
        '''Assert that clients resolves to view'''

        found = resolve('/annotation/clients/')
        self.assertEquals(found.func.view_class, views.ClientsListView)


    def test_countries_urls_resolves_to_view(self):
        '''Assert that countries resolves to view'''

        found = resolve('/annotation/countries/')
        self.assertEquals(found.func.view_class, views.CountriesListView)