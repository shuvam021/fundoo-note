from api.utils.views import CustomAuthentication
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(CustomAuthentication,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('', schema_view.with_ui(
        'swagger',
        cache_timeout=0), name='schema-swagger-ui'),
]
