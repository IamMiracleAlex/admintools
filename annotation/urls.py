from django.urls import path

from annotation import views

urlpatterns = [
    path('', views.AnnotationHandler.as_view()),
    path('reset-task/', views.ResetTask.as_view()),
    path('tbaq-count/', views.TBAQCount.as_view()),
    path('download-extension/', views.CEDownloadView.as_view()),
    path('all-urls/', views.UrlsListView.as_view()),
    path('add-url/', views.UrlsCreateView.as_view()),
    path('urls/<int:pk>/', views.UrlRetrieveView.as_view()),
    path('urls/delete/', views.UrlDeleteResetView.as_view()),
    path('urls/edit/', views.UrlUpdateView.as_view()),
    path('urls/reset/', views.UrlDeleteResetView.as_view()),
    path('assigned-urls/', views.ListAssignedUrlsView.as_view()),
    path('clients/', views.ClientsListView.as_view()),
    path('countries/', views.CountriesListView.as_view()),
    path('extension-version/', views.ExtensionVersionView.as_view()),
]
