
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('checkin/', include('checkin.urls')),
    path('leave/', include('leave.urls')),
    path('profiles/', include('profiles.urls')),
    path('admins/', include('admins.urls')),
    path('assign/', include('assign.urls')),
    
]

from django.urls import include
urlpatterns += [path('', include('account.urls'))]
