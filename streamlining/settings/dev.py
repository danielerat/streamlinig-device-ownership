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
