from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Variation
from .serializers import CategorySerializer, VariationSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public Endpoint: Returns the Category Tree.
    We only fetch 'root' categories (parent=None). 
    The Serializer recursively fetches children.
    """
    queryset = Category.objects.filter(parent_category__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


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