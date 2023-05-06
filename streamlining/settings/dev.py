from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-e^0-fym%v-z%*s0f6w=ft3^j-pocn#x)ww2^7@d2!4iwmv=(-$'


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "HOST": os.environ.get("DB_HOST"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

# Email Configurations
EMAIL_HOST = os.environ.get('GMAIL_EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('GMAIL_EMAIL_PORT', '')
EMAIL_USE_TLS = os.environ.get('GMAIL_EMAIL_USE_TLS', '')
EMAIL_HOST_USER = os.environ.get('GMAIL_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_EMAIL_HOST_PASSWORD', '')

CELERY_BROKER_URL = 'redis://localhost:6379/1'

CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        # 'schedule':contab(day_of_week=1,hours=7)
        'schedule': 5,
        'args': ['Periodic Sending of notifications']
    }
}
