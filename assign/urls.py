from django.urls import path
from . import views

urlpatterns = [
    path('assign_project/', views.assign_project, name='assign_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
]
