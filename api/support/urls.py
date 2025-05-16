from django.urls import path
from .views import CreateSupportTicketView, SupportTicketListView

urlpatterns = [
    path('create_ticket/', CreateSupportTicketView.as_view(), name='create_ticket'),
    path('tickets/', SupportTicketListView.as_view(), name='support-ticket-list'),

]
