from django.urls import include, path
from stream import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('devices', views.DeviceViewset)

urlpatterns = [
    path('', include(router.urls)),
]
