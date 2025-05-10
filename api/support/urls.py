from django.urls import path
from .views import CreateSupportTicketView

urlpatterns = [
    path('create_ticket/', CreateSupportTicketView.as_view(), name='create_ticket')
]
