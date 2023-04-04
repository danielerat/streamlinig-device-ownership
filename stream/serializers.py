from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.serializers import SimpleUserSerializer
from datetime import datetime, timedelta
from django.utils import timezone

from stream.models import Device, DeviceImage, Warranty

# warranty serializer


class WarrantySerializer(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = Warranty
        fields = ('device', 'days', 'created',
                  'remaining_days')

    def get_remaining_days(self, warranty):
        expiration_date = warranty.created + timedelta(days=warranty.days)
        remaining_days = (expiration_date - timezone.now()).days

        return {"remaining_days": max(remaining_days, 0), "percentage": "{}%".format(100-(max(remaining_days, 0)*warranty.days/100))}

# Device Image Serializer


class DeviceImageSerializer(ModelSerializer):
    class Meta:
        model = DeviceImage
        fields = ['id', 'image']

    def create(self, validated_data):
        device_pk = self.context['device_pk']
        return DeviceImage.objects.create(device_id=device_pk, **validated_data)


# Device Serializer


class DeviceSerializer(ModelSerializer):
    images = DeviceImageSerializer(many=True)
    owner = SimpleUserSerializer(read_only=True)
    warranty = WarrantySerializer(read_only=True)

    class Meta:
        model = Device
        fields = ["id", "name", "model", "serial_number", "mac_address", "imei",
                  "price", "category", "desc", "quality", "status", "owner", "images", "warranty"]
