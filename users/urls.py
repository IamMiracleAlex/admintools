from django.urls import path, include

from users import views


urlpatterns = [
    path('looker-auth/', views.LookerAuth.as_view()),
]