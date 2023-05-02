from django.urls import include, path
from stream import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('devices', views.DeviceViewset, basename='devices')
router.register('pending-devices', views.PendingDevicesViewset,
                basename='pending-devices')

devices_router = routers.NestedSimpleRouter(
    router, 'devices', lookup='device')

devices_router.register(
    'images', views.DeviceImageViewset, basename='device-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(devices_router.urls)),
    path('search/', views.DeviceSearchAPIView.as_view(), name='device-search'),
    path('report-found/', views.ReportedDeviceAPIView.as_view(), name='found-devices'),

]
