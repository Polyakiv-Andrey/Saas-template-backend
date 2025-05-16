from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.support.filters import SupportTicketFilter
from api.support.models import SupportTicket
from api.support.serializers import SupportTicketWriteSerializer, SupportTicketReadSerializer


class CreateSupportTicketView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SupportTicketWriteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            support_ticket = serializer.save(reported_by=request.user)

            return Response(
                {'message': 'Ticket created successfully', 'ticket_id': support_ticket.id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SupportTicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SupportTicketReadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SupportTicketFilter

    def get_queryset(self):
        return SupportTicket.objects.filter(reported_by=self.request.user).order_by('-created_at')

