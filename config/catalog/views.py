from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Variation,VariationOption, Brand
from .serializers import CategorySerializer, VariationSerializer, VariationOptionSerializer, BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    - List: Returns only Root Categories (Recursion handles the rest).
    - Retrieve/Update/Delete: Can access ANY Category (Root or Sub).
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        # 1. If we are asking for a LIST, only return the main parents (Roots)
        #    Sorted by Newest First (-id)
        if self.action == 'list':
            return Category.objects.filter(parent_category__isnull=True).order_by('-id')
        
        # 2. If we are Deleting/Updating/Viewing a specific ID, look through ALL categories
        return Category.objects.all().order_by('-id')


class VariationViewSet(viewsets.ModelViewSet):
    """
    Vendor Endpoint: Returns Attributes they can use.
    Logic:
    - If user is Vendor: Show Global Attributes + Their Private Attributes.
    - If user is Admin: Show everything.
    - If Anonymous: 403 Forbidden (Public doesn't need to see raw attribute lists).
    """
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Superusers see everything
        if user.is_superuser:
            return Variation.objects.all()
        
        # 2. Vendors see Global + Their Own
        if hasattr(user, 'vendor_shop'):
            return Variation.objects.filter(
                Q(is_global=True) | Q(vendor_shop=user.vendor_shop)
            )
            
        # 3. Regular users (shouldn't really access this, but fallback to global)
        return Variation.objects.filter(is_global=True)
class BrandViewSet(viewsets.ModelViewSet):
    """
    Public Endpoint: Returns list of Brands.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
class VariationOptionViewSet(viewsets.ModelViewSet):
    """
    Allows Admin to add options (S, M, L, Red) to a Variation.
    """
    queryset = VariationOption.objects.all()
    serializer_class = VariationOptionSerializer
    permission_classes = [permissions.IsAuthenticated]