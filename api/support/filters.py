import django_filters
from .models import SupportTicket


class SupportTicketFilter(django_filters.FilterSet):
    interacted = django_filters.BooleanFilter(method='filter_interacted')

    class Meta:
        model = SupportTicket
        fields = ['interacted']

    def filter_interacted(self, queryset, name, value):
        if value:
            return queryset.exclude(status='open')
        return queryset.filter(status='open')
