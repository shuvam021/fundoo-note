from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [

    path('', views.NoteViewset.as_view({
        'get': 'list', 'post': 'create'})),
    path('<int:pk>/', views.NoteViewset.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('labels/', views.LabelViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('labels/<int:pk>/', views.LabelViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
