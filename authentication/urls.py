from django.urls import path
from .views import ForgotAPIView, LogoutAPIView, RegisterAPIView, LoginAPIView, ResetAPIView, UserAPIView, RefreshAPIView, UserCheckAPIView
urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("user/", UserAPIView.as_view(), name="user"),
    path("user/check", UserCheckAPIView.as_view(), name="user-check"),
    path("refresh/", RefreshAPIView.as_view(), name="refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("forgot/", ForgotAPIView.as_view(), name="forgot"),
    path("reset/", ResetAPIView.as_view(), name="reset"),

]
