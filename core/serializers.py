from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import User


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'account_type']
