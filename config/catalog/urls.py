from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, VariationViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', VariationViewSet, basename='attribute')

urlpatterns = [
    path('', include(router.urls)),
]