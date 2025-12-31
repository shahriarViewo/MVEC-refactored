from rest_framework import serializers
from .models import Category, Brand, Variation, VariationOption

# -----------------------------
# Category Serializer
# -----------------------------
class CategorySerializer(serializers.ModelSerializer):
    # Recursively serialize children for a tree view
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'icon', 'parent_category', 'subcategories']

    def get_subcategories(self, obj):
        # Simple recursion check to avoid infinite depth if data is bad, 
        # or just standard serialization of children
        children = obj.subcategories.all()
        return CategorySerializer(children, many=True).data


# -----------------------------
# Brand Serializer
# -----------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


# -----------------------------
# Variation Option Serializer
# -----------------------------
class VariationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id', 'value', 'variation']


# -----------------------------
# Variation Serializer
# -----------------------------
class VariationSerializer(serializers.ModelSerializer):
    # Nested options allow you to see "Size" and ["S", "M", "L"] in one call
    options = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Variation
        fields = ['id', 'name', 'is_global', 'vendor_shop', 'options']