from django.urls import path, include
from .views import (
    IntentView,
    IntentChangeView,
    CorrelationView,
    CorrelationChangeView,
    SalesView,
    SalesChangeView,
    PeriodView,
)
from .views import IntentView
from .models import PriorityAction
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register("", PriorityActionView, basename=PriorityAction)

urlpatterns = [
    path("intent/", IntentView.as_view()),
    path("intent_change/", IntentChangeView.as_view()),
    path("correlation/", CorrelationView.as_view()),
    path("correlation_change/", CorrelationChangeView.as_view()),
    path("sales/", SalesView.as_view()),
    path("sales_change/", SalesChangeView.as_view()),
    path("period/", PeriodView.as_view()),
]
