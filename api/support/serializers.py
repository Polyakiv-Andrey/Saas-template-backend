from rest_framework import serializers

from api.support.models import SupportTicket


class SupportTicketWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportTicket
        fields = ["title", "description"]