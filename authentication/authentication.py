import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from core.models import User
from core.serializers import UserSerializer


def create_access_token(id):
    return jwt.encode(
        {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }, 'access_secret', algorithm='HS256'
    )
