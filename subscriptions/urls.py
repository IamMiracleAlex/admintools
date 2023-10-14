from django.conf.urls import url
from django.urls import path, include
from .views import SubscriptionView, DagView
from .models import Subscription
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", SubscriptionView, "subscription")

urlpatterns = [
    path("dag/", DagView.as_view()),
    path("<client_id>/", include(router.urls)),
    ]