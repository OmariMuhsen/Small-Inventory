# backend/inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, SupplierViewSet, LocationViewSet,
    PersonViewSet, ItemViewSet, MaintenanceRecordViewSet,
    TransactionViewSet, DashboardViewSet
)

router = DefaultRouter()

# Register viewsets with the router
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'maintenance-records', MaintenanceRecordViewSet, basename='maintenancerecord')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# Custom URLs that don't fit the ViewSet pattern
custom_urlpatterns = [
    path('items/<int:pk>/checkout/', ItemViewSet.as_view({'post': 'checkout'}), name='item-checkout'),
    path('items/<int:pk>/checkin/', ItemViewSet.as_view({'post': 'checkin'}), name='item-checkin'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + custom_urlpatterns

# Optional: Add API documentation URLs (requires drf-yasg or drf-spectacular)
try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    ]
except ImportError:
    pass