from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="AMBASSADORS API",
        default_version="v1",
        decription="Welcome to the ambassadors api",
        terms_of_service="https://www.datadevpro.com",
        contact=openapi.Contact(email="emmanoedorh@gmail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/admin/', include("administrator.urls")),
    path('api/ambassador/', include("ambassador.urls")),
    path('api/checkout/', include("checkout.urls")),

]
