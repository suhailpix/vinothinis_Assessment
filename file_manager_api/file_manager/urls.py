from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('list_files/', views.list_files, name='list_files'),
    path('delete_files/', views.delete_files, name='delete_files'),
    path('retrieve_files/', views.retrieve_files, name='retrieve_files'),
    path('restore_files/', views.restore_files, name='restore_files'),
]
