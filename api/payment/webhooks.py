import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import PaymentMethod
from api.subscription.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_method.attached':
        handle_payment_method_attached(event.data.object)
    elif event.type == 'payment_method.detached':
        handle_payment_method_detached(event.data.object)
    elif event.type == 'customer.subscription.updated':
        handle_subscription_updated(event.data.object)
    elif event.type == 'customer.subscription.deleted':
        handle_subscription_deleted(event.data.object)
    elif event.type == 'invoice.payment_failed':
        handle_payment_failed(event.data.object)

    return HttpResponse(status=200)


def handle_payment_method_attached(payment_method_data):
    try:
        PaymentMethod.objects.create(
            user_id=payment_method_data.metadata.get('user_id'),
            stripe_payment_method_id=payment_method_data.id,
            is_default=payment_method_data.metadata.get('is_default', False)
        )
    except Exception:
        pass


def handle_payment_method_detached(payment_method_data):
    try:
        PaymentMethod.objects.filter(
            stripe_payment_method_id=payment_method_data.id
        ).delete()
    except Exception:
        pass


def handle_subscription_updated(subscription_data):
    try:
        subscription = Subscription.objects.get(
            stripe_subscription_id=subscription_data.id
        )
        subscription.status = subscription_data.status
        subscription.current_period_start = subscription_data.current_period_start
        subscription.current_period_end = subscription_data.current_period_end
        subscription.cancel_at_period_end = subscription_data.cancel_at_period_end
        subscription.save()
    except Subscription.DoesNotExist:
        pass


def handle_subscription_deleted(subscription_data):
    try:
        subscription = Subscription.objects.get(
            stripe_subscription_id=subscription_data.id
        )
        subscription.status = 'canceled'
        subscription.save()
    except Subscription.DoesNotExist:
        pass


def handle_payment_failed(invoice_data):
    try:
        subscription = Subscription.objects.get(
            stripe_subscription_id=invoice_data.subscription
        )
        subscription.status = 'past_due'
        subscription.save()
    except Subscription.DoesNotExist:
        pass
