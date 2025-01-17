from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:profile_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:profile_id>/', views.delete_employee, name='delete_employee'),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/', views.events, name='events'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:user_id>/', views.chat, name='chat_with_user'),
]