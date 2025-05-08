from django.urls import path
from .views import PaymentMethodListView
from .webhooks import stripe_webhook

urlpatterns = [
    path('payment-methods/', PaymentMethodListView.as_view(), name='payment-methods'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
] 