from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .models import Product, ProductVariant, ProductImage
from .serializers import ProductSerializer, ProductVariantSerializer, ProductImageSerializer
from .permissions import IsVendorOwner
from .models import ProductVideo
from .serializers import ProductVideoSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Main Product API.
    - Public: See 'Active' products.
    - Vendor: See all their own products (Draft, Pending, Active).
    """
    serializer_class = ProductSerializer
    # Use IsAuthenticatedOrReadOnly so public can see, but only logged in can create
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsVendorOwner]
    
    # Enable search and filter
    filterset_fields = ['category', 'brand', 'status', 'vendor_shop']
    search_fields = ['product_name', 'short_description']

    def get_queryset(self):
        user = self.request.user
        
        # 1. Base Query: Public sees only Active products
        queryset = Product.objects.filter(status='active')
        
        # 2. If Vendor is logged in, they also see THEIR OWN non-active products
        if user.is_authenticated and hasattr(user, 'vendor_shop'):
            my_products = Product.objects.filter(vendor_shop=user.vendor_shop)
            # Combine the lists (public active + my own)
            queryset = (queryset | my_products).distinct()
            
        return queryset

    def perform_create(self, serializer):
        # Automatically assign the logged-in user's shop to the product
        if not hasattr(self.request.user, 'vendor_shop'):
            raise permissions.PermissionDenied("You must be a Vendor to create products.")
        serializer.save(vendor_shop=self.request.user.vendor_shop)


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    API for managing specific SKUs (e.g., Red-XL, Blue-S).
    """
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter variants by the product_id passed in the URL
        return ProductVariant.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        # Ensure the product belongs to the request user before adding a variant
        product_id = self.kwargs['product_pk']
        product = Product.objects.get(pk=product_id)
        
        if product.vendor_shop != self.request.user.vendor_shop:
             raise permissions.PermissionDenied("You cannot add variants to another vendor's product.")
             
        serializer.save(product_id=product_id)


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API for uploading images.
    """
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] # To handle file uploads

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        product = Product.objects.get(pk=product_id)
        
        if product.vendor_shop != self.request.user.vendor_shop:
             raise permissions.PermissionDenied("You cannot upload images to another vendor's product.")
        
        serializer.save(product_id=product_id)



class ProductVideoViewSet(viewsets.ModelViewSet):
    """
    API for uploading Product Videos.
    """
    serializer_class = ProductVideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return ProductVideo.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        product = Product.objects.get(pk=product_id)
        
        # Check ownership
        if product.vendor_shop != self.request.user.vendor_shop:
             raise permissions.PermissionDenied("You cannot upload videos to another vendor's product.")
        
        serializer.save(product_id=product_id)