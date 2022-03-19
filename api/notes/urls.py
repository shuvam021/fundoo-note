from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [

    path('', views.NoteViewset.as_view({
        'get': 'list', 'post': 'create'}), name='note'),
    path('<int:pk>/', views.NoteViewset.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='note-details'),
]
