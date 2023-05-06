import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamlining.settings.dev')

celery = Celery('streamlining')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
