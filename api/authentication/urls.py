from unicodedata import name

from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.UserViewSet.as_view({'get': 'list'}), name='users'),
    path('<int:pk>/', views.UserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'delete'}), name='user-details'),
]
