from django.conf import settings
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
import re

from stream.models import Device, DeviceFirstAssignment, DeviceImage, PendingTransfer, ReportedDevice, Transfer, Warranty
from authentication.models import User

from rest_framework.exceptions import APIException


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ["id", "transferor", "transferee", "last_confirm", "created"]

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
    images = DeviceImageSerializer(many=True, read_only=True)
    warranty = WarrantySerializer(read_only=True)
    transfers = TransferSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ["id", "name", "model", "serial_number", "mac_address", "imei", "price",
                  "category", "desc", "quality", "status", "owner", "images", "warranty", "transfers"]

    def create(self, validated_data):
        request = self.context.get('request')
        with transaction.atomic():
            device, created = Device.objects.get_or_create(**validated_data)
            # if device is not being saved for the first time, update the existing instance
            if created:
                device.save()
                DeviceFirstAssignment.objects.create(
                    device_id=device.pk, holder=request.user, first_owner=device.owner)
            return device


class DeviceTransferSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        min_length=10, max_length=10, allow_blank=False)

    national_id = serializers.CharField(
        max_length=16)

    def validate(self, data):
        device_pk = self.context.get('device_pk')
        user = self.context.get('request').user
        if not re.match(r'^\d{16}$', data['national_id']):
            raise serializers.ValidationError('Invalid National ID',
                                              status_code=status.HTTP_400_BAD_REQUEST)
        elif not re.match(r'^\d{10}$', data['phone_number']):
            raise serializers.ValidationError('Phone Number is Invalid',
                                              status_code=status.HTTP_400_BAD_REQUEST)
        elif not Device.objects.filter(id=device_pk).exists():
            raise serializers.ValidationError(
                'An unknown Device is Being Transferred.', status_code=status.HTTP_400_BAD_REQUEST)
        elif not User.objects.filter(phone_number=data['phone_number'], national_id=data['national_id']).exists():
            raise serializers.ValidationError(
                'You Are trying to transfer a device to an unknown User.')
        elif not Device.objects.filter(id=device_pk, owner=user.id).exists():
            raise serializers.ValidationError(
                "You can not Transfer This device.")

        return data

        #     raise APIException("You can not transfer a device that does not belong to you",
        #                        status_code=status.HTTP_401_UNAUTHORIZED)

    def save(self, **kwargs):
        device_pk = self.context.get('device_pk')
        phone_number = self.validated_data['phone_number']
        national_id = self.validated_data['national_id']
        transferor = self.context.get('request').user
        # If one fails then other fails too.
        with transaction.atomic():
            # We have a cart item, Update it.
            device = Device.objects.get(id=device_pk)
            owner = User.objects.get(
                phone_number=phone_number, national_id=national_id)
            PendingTransfer.objects.create(
                device=device, transferor=transferor, transferee=owner)
            self.instance = device
        return self.instance


class ReportedDeviceSerializer(ModelSerializer):
    device = serializers.CharField(max_length=64)

    class Meta:
        model = ReportedDevice
        fields = ['device', 'names', 'phone_number', 'comment']

    def create(self, validated_data):
        reported = ReportedDevice.objects.create(**validated_data)
        return True

    def validate(self, data):
        search_query = data['device']
        device = Device.objects.filter(Q(imei=search_query) | Q(
            serial_number=search_query) | Q(mac_address=search_query), Q(status='stolen') | Q(status='lost'))
        if not device.exists():
            raise serializers.ValidationError(
                "This Device is not reported lost.")
        data['device'] = device.first()
        return data
