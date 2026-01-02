from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductVariantViewSet, ProductImageViewSet, ProductVideoViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

variant_router = DefaultRouter()
variant_router.register(r'variants', ProductVariantViewSet, basename='product-variants')

image_router = DefaultRouter()
image_router.register(r'images', ProductImageViewSet, basename='product-images')

video_router = DefaultRouter()
video_router.register(r'videos', ProductVideoViewSet, basename='product-videos')

urlpatterns = [
    path('', include(router.urls)),
    
    path('products/<int:product_pk>/', include(variant_router.urls)),
    
    path('products/<int:product_pk>/', include(image_router.urls)),
    
    path('products/<int:product_pk>/', include(video_router.urls)),
]