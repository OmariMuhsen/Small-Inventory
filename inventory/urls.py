# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    # Admin Site URLs (protected with admin auth)
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='api-docs'),
    path('api/schema/', get_schema_view(
        title="Inventory System API",
        description="API for the Inventory Management System",
        version="1.0.0"
    ), name='openapi-schema'),
    
    # API Version 1
    path('api/v1/', include([
        # Authentication
        path('auth/', include('rest_framework.urls', namespace='rest_framework')),
        
        # Inventory App
        path('inventory/', include('inventory.urls')),
        
        # Add other apps here as needed
        # path('another-app/', include('another_app.urls')),
    ])),
    
    # Frontend Fallback (for SPA integration)
    path('', TemplateView.as_view(template_name='index.html')),
]

# Development-only URLs
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Admin Site Titles
admin.site.site_header = "Inventory System Administration"
admin.site.site_title = "Inventory System Admin Portal"
admin.site.index_title = "Welcome to Inventory System Admin"