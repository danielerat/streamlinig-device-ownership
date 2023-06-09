from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from stream.models import Device, DeviceImage, PendingTransfer, Transfer
from stream.permissions import IsBusinessOwnerOrReadOnly

from stream.serializers import DeviceImageSerializer, DeviceSerializer, DeviceTransferSerializer, PendingDeviceSerializer, ReportedDeviceSerializer, TransfersSerializer
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# --- Ninja Views---


class DeviceViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.filter(owner=self.request.user)
        return queryset
    # An action responsible of transferring a given device to a given user.
        # devices/transfer

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        serializer = DeviceTransferSerializer(
            data=request.data, context={"device_pk": self.kwargs['pk'], "request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Device Successfully Tranfered'})
    # Action to get all the devices I ever transferred.
        # devices/my_transfers

    @action(detail=False, methods=['get'])
    def my_transfers(self, request):
        devices = Transfer.objects.filter(
            Q(transferor=request.user) |
            Q(transferee=request.user)
        )
        serializer = TransfersSerializer(devices, many=True)
        return Response(serializer.data)


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


class ReportedDeviceAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        data = request.data
        serializer = ReportedDeviceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("ok")


class StatView(APIView):
    # return statistical data here
    pass


class PendingDevicesViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PendingDeviceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = PendingTransfer.objects.filter(transferee=user)
        return queryset
