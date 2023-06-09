from .common import *
import os

DEBUG = False
ALLOWED_HOSTS = ['streamlining.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASE_URL = os.getenv('JAWSDB_URL')

database_attr = DATABASE_URL.split(':')

JaName = database_attr[3].split('/')[1].rstrip("'")
JaUser = database_attr[1].lstrip('//')
JaPwrd = database_attr[2].split('@')[0]
JaHost = database_attr[2].split('@')[1]
JaPort = int(database_attr[3].split('/')[0])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': JaName,
        'USER': JaUser,
        'PASSWORD': JaPwrd,
        'HOST': JaHost,
    }
}

# Email Configurations


EMAIL_HOST = os.environ.get('GMAIL_EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('GMAIL_EMAIL_PORT', '')
EMAIL_USE_TLS = os.environ.get('GMAIL_EMAIL_USE_TLS', '')
EMAIL_HOST_USER = os.environ.get('GMAIL_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_EMAIL_HOST_PASSWORD', '')
