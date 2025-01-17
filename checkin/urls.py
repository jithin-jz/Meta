from django.urls import path
from . import views

urlpatterns = [
    path("attendance_view/", views.attendance_view, name="attendance_view"),
]