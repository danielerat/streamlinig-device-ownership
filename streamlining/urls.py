from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView  #new
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="stream/index.html")),
    path('admin/', admin.site.urls),
    path('streamlining/v1/', include('stream.urls')),
    path('streamlining/v1/auth/', include('authentication.urls')),

    # Api Documentation Schema
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), #new
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
