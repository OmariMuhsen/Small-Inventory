# project-level urls.py (e.g., myproject/urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invent/', include('invent.urls')),  # Include inventory app URLs here
    path('', include('core.urls')),  # Include core app URLs here
]
