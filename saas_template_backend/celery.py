import os
from celery import Celery
from celery.schedules import crontab

from saas_template_backend import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas_template_backend.settings')

app = Celery('saas_template_backend', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
