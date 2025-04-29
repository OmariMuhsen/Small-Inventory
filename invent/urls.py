from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, PersonViewSet, CategoryViewSet, CustomAuthToken

router = DefaultRouter()

router.register(r'people', PersonViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'items', views.ItemViewSet)  # ✅ No parentheses!


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomAuthToken.as_view(), name='api-token'),
]
