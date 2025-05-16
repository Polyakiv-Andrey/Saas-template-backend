from django.urls import path
from .views import PaymentMethodListView, CreateBillingPortalSession
from .webhooks import stripe_webhook

urlpatterns = [
    path('payment-methods/', PaymentMethodListView.as_view(), name='payment-methods'),
    path('billing-portal/', CreateBillingPortalSession.as_view(), name='billing-portal'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
