from django.urls import path
from custom_admin import views

urlpatterns = [
    path('bulk-edit/', views.HandleBulkEdit.as_view(), name="bulk_edit"),
    path('load-extra-data/', views.load_extra_data, name="load_extra_data"),
    path('facet_bulk_edit/', views.HandleFacetBulkEdit.as_view(), name='facet_bulk_edit'),
    path('data_release/', views.HandleDataRelease.as_view(), name='data_release'),
    path('row-data/', views.get_row_data, name="row_data")
]