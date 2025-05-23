from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, MaintenanceRecordViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'maintenance-records', MaintenanceRecordViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
