import os
from celery import Celery
from celery.schedules import crontab

from core import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
