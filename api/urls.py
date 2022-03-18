from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from api.authentication import views

app_name = 'api'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('verify/<str:token>/', views.UserVerify.as_view(), name='verify'),
    path('auth/', include('api.authentication.urls', namespace='auth')),
]
