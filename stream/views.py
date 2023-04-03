from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from stream.models import Device

from stream.serializers import DeviceSerializer

# --- Ninja Views---


class DeviceViewset(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
