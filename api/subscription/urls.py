from django.urls import path
from .views import (
    SubscriptionPlanListView,
    SubscriptionView
)

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]
