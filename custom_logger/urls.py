from django.urls import path

from custom_logger.views import ChromeExtensionLogView


urlpatterns = [
    path('chrome', ChromeExtensionLogView.as_view()),
]
