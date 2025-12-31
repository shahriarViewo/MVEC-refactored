from rest_framework import serializers
from .models import Category, Brand, Variation, VariationOption
from accounts.serializers import ImageSerializer

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
# Variation Option Serializer (THE MISSING PART)
# -----------------------------
class VariationOptionSerializer(serializers.ModelSerializer):
    # Shows the full image object if a pattern is uploaded
    pattern_image_details = ImageSerializer(source='pattern_image', read_only=True)

    class Meta:
        model = VariationOption
        # Added color_code and pattern_image
        fields = ['id', 'value', 'color_code', 'pattern_image', 'pattern_image_details']


# -----------------------------
# Variation Serializer
# -----------------------------
class VariationSerializer(serializers.ModelSerializer):
    # Nested options allow you to see "Size" and ["S", "M", "L"] in one call
    options = VariationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Variation
        # Added display_mode
        fields = ['id', 'name', 'is_global', 'display_mode', 'vendor_shop', 'options']