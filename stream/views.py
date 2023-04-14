from django.http import Http404
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from stream.models import Device, DeviceImage
from rest_framework.generics import ListAPIView
from stream.serializers import DeviceImageSerializer, DeviceSerializer, DeviceTransferSerializer
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# --- Ninja Views---


class DeviceViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        serializer = DeviceTransferSerializer(
            data=request.data, context={"device_pk": self.kwargs['pk'], "request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Device Successfully Tranfered'})

    def get_serializer_context(self):
        return {"request": self.request}


class DeviceImageViewset(ModelViewSet):
    serializer_class = DeviceImageSerializer

    def get_queryset(self):
        return DeviceImage.objects.filter(device_id=self.kwargs['device_pk'])

    def get_serializer_context(self):
        # Get the image id and send it in the backend
        return {"device_pk": self.kwargs["device_pk"], "user": self.request.user}


class DeviceSearchAPIView(APIView):
    def get(self, request):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Search for devices with matching IMEI, serial number, or MAC address in a single query
            devices = Device.objects.filter(Q(imei=search_query) | Q(
                serial_number=search_query) | Q(mac_address=search_query))

            # Check if any devices were found
            if devices.exists():
                # Get the first device from the queryset
                device = devices.first()

                # Check if the device is reported as stolen, active, or lost
                if device.status == 'stolen':
                    # Return warning message as an error response
                    return Response({'message': 'Device reported as stolen', 'status': device.status, 'device': {'name': device.name, 'category': device.category}}, status=status.HTTP_200_OK)
                elif device.status == 'active':
                    # Return binary response indicating device is not reported as stolen
                    return Response({'message': 'Device not reported as stolen', 'status': device.status, 'device': {'name': device.name, 'category': device.category}}, status=status.HTTP_200_OK)
                elif device.status == 'lost':
                    # Return binary response indicating device is not reported as stolen
                    return Response({'message': 'Device Reported Lost.', 'status': device.status, 'device': {'name': device.name, 'category': device.category}}, status=status.HTTP_200_OK)
            else:
                # Return binary response indicating device not found
                return Response({'message': 'Device not registered in the system, thus not reported as stolen.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': "Search for a device using its serial number, IMEI, or MAC address, and I will tell you whether it's safe to buy or not. (/search/?search='ime/mac/searial')"}, status=status.HTTP_200_OK)
