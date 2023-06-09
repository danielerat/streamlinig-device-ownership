from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'national_id', 'password', 'devices']
        extra_kwargs = {
            'password': {'write_only': True},
            'devices': {'read_only': True}
        }

    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password', None)
        # Create instance
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # Set the password using django builtin funciton
            instance.set_password(password)
        instance.save()
        return instance
