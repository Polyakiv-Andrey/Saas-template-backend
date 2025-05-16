import django_filters
from .models import SupportTicket


class SupportTicketFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=SupportTicket.TICKET_STATUSES,
        lookup_expr='iexact',
    )

    class Meta:
        model = SupportTicket
        fields = ['status']
