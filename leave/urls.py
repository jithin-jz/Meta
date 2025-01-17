from django.urls import path
from . import views

urlpatterns = [
    path("leave/", views.leave, name="leave"),
]