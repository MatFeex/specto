from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('configuration.urls')),
    path('',include('vms.urls')),
    path('',include('vmq.urls')),
    path('',include('gemba.urls')),
]
