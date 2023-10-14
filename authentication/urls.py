from django.conf.urls import url
from django.urls import path, include
from authentication.views import GoogleAuthView


urlpatterns = [
    path('login/', GoogleAuthView.as_view()),
    ]