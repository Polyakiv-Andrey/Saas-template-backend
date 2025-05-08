from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.authentication.urls')),
    path('payment/', include('api.payment.urls')),
    path('subscription/', include('api.subscription.urls')),
]
