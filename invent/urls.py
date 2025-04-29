# backend/inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, PersonViewSet, CategoryViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'people', PersonViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
]