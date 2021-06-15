from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    UserAPIView,
    LogoutAPIView,
    ProfileInfoAPIView,
    ProfilePasswordAPIView,
)


urlpatterns = [
    path("register", RegisterAPIView.as_view()),
    path("login", LoginAPIView.as_view()),
    path("user", UserAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
    path("user/info", ProfileInfoAPIView.as_view()),
    path("user/password", ProfilePasswordAPIView.as_view()),
]