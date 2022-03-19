from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from api.authentication import views
from api.notes.views import LabelViewSet

app_name = 'api'

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/<str:token>/', views.UserVerify.as_view(), name='verify'),
    path('forget_password/', views.ForgetPasswordAPIView.as_view(), name='forget_password'),
    path('update_password/<str:token>/', views.UpdatePasswordAPIView.as_view(), name='update_password'),

    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('user/', include('api.authentication.urls', namespace='auth')),
    path('notes/', include('api.notes.urls', namespace='note')),

    path('labels/', LabelViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='label'),
    path('labels/<int:pk>/', LabelViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='label-details'),

]
