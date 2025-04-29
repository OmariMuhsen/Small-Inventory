from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SupplierViewSet, LocationViewSet, PersonViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'people', PersonViewSet)

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
