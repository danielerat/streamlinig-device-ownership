from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from stream.models import Device, DeviceImage

from stream.serializers import DeviceImageSerializer, DeviceSerializer

# --- Ninja Views---


class DeviceViewset(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceImageViewset(ModelViewSet):
    serializer_class = DeviceImageSerializer

    def get_queryset(self):
        return DeviceImage.objects.filter(device_id=self.kwargs['device_pk'])

    def get_serializer_context(self):
        # Get the image id and send it in the backend
        return {"device_pk": self.kwargs["device_pk"]}
