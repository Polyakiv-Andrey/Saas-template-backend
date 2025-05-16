import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from saas_template_backend.settings import SUBSCRIPTION_RETURN_URL
from .models import PaymentMethod
from .serializers import PaymentMethodSerializer
from ..subscription.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentMethodListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return Response(serializer.data)


class CreateBillingPortalSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            sub = Subscription.objects.filter(user=request.user, status="active").first()
            if not sub:
                return Response({'detail': 'No subscription found'}, status=status.HTTP_404_NOT_FOUND)
            customer_id = sub.stripe_customer_id
        except Subscription.DoesNotExist:
            return Response({'detail': 'No subscription found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=SUBSCRIPTION_RETURN_URL
            )
        except stripe.error.StripeError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'url': session.url}, status=status.HTTP_200_OK)