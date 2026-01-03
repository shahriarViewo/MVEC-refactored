from rest_framework import serializers
from .models import Category, Brand, Variation, VariationOption
# Ensure this import path is correct for your project
from accounts.serializers import ImageSerializer 

# -----------------------------
# Category Serializer
# -----------------------------
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'icon', 'parent_category', 'subcategories']

    def get_subcategories(self, obj):
        # Sort sub-categories by Newest First (-id)
        children = obj.subcategories.all().order_by('-id')
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
    pattern_image_details = ImageSerializer(source='pattern_image', read_only=True)
    
    class Meta:
        model = VariationOption
        fields = ['id', 'variation', 'value', 'color_code', 'pattern_image', 'pattern_image_details']


# -----------------------------
# Variation Serializer
# -----------------------------
class VariationSerializer(serializers.ModelSerializer):
    options = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Variation
        fields = ['id', 'name', 'is_global', 'display_mode', 'vendor_shop', 'options']