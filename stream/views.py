from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from stream.models import Device, DeviceImage

from stream.serializers import DeviceImageSerializer, DeviceSerializer, DeviceTransferSerializer

from rest_framework.decorators import action

from rest_framework.response import Response
# --- Ninja Views---


class DeviceViewset(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        serializer = DeviceTransferSerializer(
            data=request.data, context={"device_pk": self.kwargs['pk'], "request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Device Successfully Tranfered'})


class DeviceImageViewset(ModelViewSet):
    serializer_class = DeviceImageSerializer

    def get_queryset(self):
        return DeviceImage.objects.filter(device_id=self.kwargs['device_pk'])

    def get_serializer_context(self):
        # Get the image id and send it in the backend
        return {"device_pk": self.kwargs["device_pk"], "user": self.request.user}
