from django.urls import path
from .views import PrivacyPolicyView, TermsOfServiceView

urlpatterns = [
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms/', TermsOfServiceView.as_view(), name='terms-of-service'),

]