from rest_framework import serializers
from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'stripe_payment_method_id', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at'] 