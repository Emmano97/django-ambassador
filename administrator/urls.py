from django.urls import path, include

from administrator.views import (
    AmbassadorAPIView,
    ProductGenericAPIView,
    OrderAPIView,
    LinkAPIView,
)

urlpatterns = [
    path("", include('common.urls')),
    path("ambassadors", AmbassadorAPIView.as_view()),
    path("products/<str:pk>", ProductGenericAPIView.as_view()),
    path("products", ProductGenericAPIView.as_view()),
    path("user/<str:pk>/links", LinkAPIView.as_view()),
    path("orders", OrderAPIView.as_view()),
]