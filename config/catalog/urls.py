from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, VariationViewSet, BrandViewSet, VariationOptionViewSet
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', VariationViewSet, basename='attribute')
router.register(r'options', VariationOptionViewSet, basename='option')
router.register('brands', BrandViewSet)
urlpatterns = [
    path('', include(router.urls)),
]