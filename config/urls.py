from api.utils.views import CustomAuthentication
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.generic import TemplateView
from core.views import fbv_login_view, fbv_logout_view, UserResister

schema_view = get_schema_view(
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(CustomAuthentication,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('docs/', schema_view.with_ui(
        'swagger',
        cache_timeout=0), name='schema-swagger-ui'),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('login/', fbv_login_view, name='custom-login'),
    path('logout/', fbv_logout_view, name='custom-logout'),
    path('register/', UserResister.as_view(), name='create-user'),
]
