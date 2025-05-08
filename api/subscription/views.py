from datetime import datetime

import stripe
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionPlan, Subscription
from .serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    CreateSubscriptionSerializer,
)
from .utils import stripe_error

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionPlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        default_plans = [
            {
                "id": 1,
                "name": "Basic Plan",
                "price": 10.00,
                "currency": "usd",
                "interval": "month",
                "stripe_price_id": "price_1RMZT9KeFoXYlmxIG0vQ5T4u",
                "features": {"feature_1": "basic_feature", "feature_2": "basic_support"},
            },
            {
                "id": 2,
                "name": "Standard Plan",
                "price": 30.00,
                "currency": "usd",
                "interval": "month",
                "stripe_price_id": "price_1RMWF8KeFoXYlmxIsPtwkNaf",
                "features": {"feature_1": "standard_feature", "feature_2": "priority_support"},
            },
            {
                "id": 3,
                "name": "Premium Plan",
                "price": 50.00,
                "currency": "usd",
                "interval": "month",
                "stripe_price_id": "price_1RMZTMKeFoXYlmxIdGwxqgDz",
                "features": {"feature_1": "premium_feature", "feature_2": "24/7_support"},
            },
        ]
        if not plans.exists():
            for plan_data in default_plans:
                SubscriptionPlan.objects.create(**plan_data)

            plans = SubscriptionPlan.objects.filter(is_active=True)

        serializer = SubscriptionPlanSerializer(plans, many=True)

        for plan in plans:
            for default_plan in default_plans:
                if plan.id == default_plan['id']:
                    if (
                            plan.name != default_plan['name'] or
                            plan.price != default_plan['price'] or
                            plan.features != default_plan['features'] or
                            plan.stripe_price_id != default_plan['stripe_price_id']
                    ):
                        plan.name = default_plan['name']
                        plan.price = default_plan['price']
                        plan.features = default_plan['features']
                        plan.stripe_price_id = default_plan['stripe_price_id']
                        plan.save()
        return Response(serializer.data)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(
            user=request.user,
            current_period_end__gt=datetime.now()
        ).order_by('-created_at').first()

        if subscription is None:
            return Response(
                {'message': 'No active subscription found'},
                status=status.HTTP_200_OK
            )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = SubscriptionPlan.objects.get(id=serializer.validated_data['plan_id'])

            try:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    payment_method=serializer.validated_data['payment_method_id'],
                    invoice_settings={
                        'default_payment_method': serializer.validated_data['payment_method_id']
                    },
                )
            except stripe.error.StripeError as e:
                return Response(
                    {'error': stripe_error(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[{'price': plan.stripe_price_id}],
                    expand=['latest_invoice', 'items.data'],
                )
                item = subscription['items']['data'][0]

                current_period_start = item.get('current_period_start')
                current_period_end = item.get('current_period_end')
                if current_period_start:
                    current_period_start = datetime.fromtimestamp(current_period_start)

                if current_period_end:
                    current_period_end = datetime.fromtimestamp(current_period_end)

            except stripe.error.StripeError as e:
                return Response(
                    {'error': stripe_error(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.objects.create(
                user=request.user,
                plan=plan,
                status=subscription.status,
                stripe_subscription_id=subscription.id,
                stripe_customer_id=customer.id,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
            )
            return Response({
                'subscription_id': subscription.id,
                'status': subscription.status,
            })

        except SubscriptionPlan.DoesNotExist:
            return Response(
                {'error': 'Plan not found'},
                status=status.HTTP_404_NOT_FOUND
            )
