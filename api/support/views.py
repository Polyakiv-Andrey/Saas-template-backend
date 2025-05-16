from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.support.serializers import SupportTicketWriteSerializer


class CreateSupportTicketView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SupportTicketWriteSerializer(data=request.data)

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


