from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('get-status/', views.StatusView.as_view()),
    path('url_stats_view/', views.UrlStatsView.as_view()),
    path('data-status/', views.DataStatusView.as_view()),
    path('verify-email', views.verify_email_for_ses)
]
