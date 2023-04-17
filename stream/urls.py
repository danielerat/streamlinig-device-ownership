from django.urls import include, path
from stream import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('devices', views.DeviceViewset, basename='devices')

devices_router = routers.NestedSimpleRouter(
    router, 'devices', lookup='device')

devices_router.register(
    'images', views.DeviceImageViewset, basename='device-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(devices_router.urls)),
    path('search/', views.DeviceSearchAPIView.as_view(), name='device-search'),
    path('report-found/', views.ReportedDeviceAPIView.as_view(), name='found-devices'),
    path('send_email/', views.send_email, name='send_email'),
]
