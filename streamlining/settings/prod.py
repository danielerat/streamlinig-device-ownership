from .common import *
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['streamlining.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']


DATABASES = {
    "default": dj_database_url.config()
}

# Email Configurations
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = EMAIL_HOST = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
DEFAULT_FROM_EMAIL = "info@streamlining.com"
