from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from stream.models import Device, DeviceImage

# Device Image Serializer


class DeviceImageSerializer(ModelSerializer):
    class Meta:
        model = DeviceImage
        fields = ['id', 'image']

# Device Serializer


class DeviceSerializer(ModelSerializer):
    # images=DeviceImageSerializer()
    class Meta:
        model = Device
        fields = ["id", "name", "model", "serial_number", "mac_address", "imei",
                  "price", "category", "desc", "quality", "status", "owner", "images"]
