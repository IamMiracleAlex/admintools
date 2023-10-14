from django.urls import path, include

from .views import ArchiveView

urlpatterns = [
    path('', ArchiveView.as_view()),
]
