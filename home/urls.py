from django.urls import path
from . import views 

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    
    
    
]
