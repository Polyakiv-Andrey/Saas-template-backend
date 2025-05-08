from rest_framework import serializers
from .models import SubscriptionPlan, Subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price', 'currency', 'interval', 'features', 'is_active']
        read_only_fields = ['id']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'plan', 'status', 'stripe_subscription_id',
            'current_period_start', 'current_period_end',
            'cancel_at_period_end', 'created_at'
        ]
        read_only_fields = ['id', 'stripe_subscription_id', 'current_period_start', 'current_period_end']


class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    payment_method_id = serializers.CharField()
