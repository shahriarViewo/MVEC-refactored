from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductVariantViewSet, ProductImageViewSet

# 1. Main Router for Products
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# 2. Separate Routers for the Nested parts
# We will manually map these in urlpatterns below
variant_router = DefaultRouter()
variant_router.register(r'variants', ProductVariantViewSet, basename='product-variants')

image_router = DefaultRouter()
image_router.register(r'images', ProductImageViewSet, basename='product-images')

urlpatterns = [
    # API for /products/
    path('', include(router.urls)),
    
    # API for /products/1/variants/
    path('products/<int:product_pk>/', include(variant_router.urls)),
    
    # API for /products/1/images/
    path('products/<int:product_pk>/', include(image_router.urls)),
]