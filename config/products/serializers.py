from rest_framework import serializers
from .models import Product, ProductVariant, ProductImage, ProductVideo, ProductSEOConfig, DownloadableProduct
from catalog.serializers import CategorySerializer, BrandSerializer, VariationOptionSerializer
from accounts.serializers import ImageSerializer

# -----------------------------
# Media Serializers
# -----------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    image_details = ImageSerializer(source='image', read_only=True)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_details']

class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = '__all__'

# -----------------------------
# Variant Serializer
# -----------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    # Read: Full nested details of options (e.g., Color: Red)
    variation_options_details = VariationOptionSerializer(source='variation_options', many=True, read_only=True)
    
    # Write: List of IDs
    variation_options = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True # Usually set via View logic or separate write serializer
    ) 

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'price', 'stock_qty', 'variation_options', 'variation_options_details']


# -----------------------------
# SEO Serializer
# -----------------------------
class ProductSEOConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSEOConfig
        fields = ['meta_title', 'meta_description', 'canonical_url', 'tags']


# -----------------------------
# Main Product Serializer
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    # Nested Read Fields
    category_details = CategorySerializer(source='category', read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)
    
    # Nested Relations (Many-to-Many or Reverse FK)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    seo_config = ProductSEOConfigSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'vendor_shop', 'product_name', 'slug', 'short_description', 'description',
            'category', 'category_details',
            'brand', 'brand_details',
            'trending', 'featured', 'status', 'is_virtual',
            'weight_name', 'weight_value', 'length', 'width', 'height',
            'variants', 'images', 'seo_config',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor_shop', 'created_at', 'updated_at'] 
        # vendor_shop is usually set automatically in the view based on the logged-in user