from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('leave/', include('leave.urls')), 
    path('profiles/', include('profiles.urls')),
    path('admins/', include('admins.urls')), 
    path('checkin/', include('checkin.urls')),
    path('assign/', include('assign.urls')),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

