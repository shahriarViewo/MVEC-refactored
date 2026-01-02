from rest_framework import serializers
from django.utils.text import slugify
from .models import Product, ProductVariant, ProductImage, ProductVideo, ProductSEOConfig
# Critical Imports: We need the Model for validation and the Serializer for display
from catalog.models import VariationOption
from catalog.serializers import CategorySerializer, BrandSerializer, VariationOptionSerializer
from accounts.serializers import ImageSerializer
from accounts.models import Image 

# -----------------------------
# Media Serializers
# -----------------------------
# accounts/models.py must be imported to create the Image

class ProductImageSerializer(serializers.ModelSerializer):
    image_details = ImageSerializer(source='image', read_only=True)
    
    # NEW: Accept a raw file upload (Write Only)
    file_upload = serializers.ImageField(write_only=True, required=True)
    
    # Make the original ID field read-only (it will be auto-filled)
    image = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'file_upload', 'variant', 'image_details']

    def create(self, validated_data):
        # 1. Pop the file from the data
        file_obj = validated_data.pop('file_upload')
        
        # 2. Create the Base Image (using correct fields from accounts/models.py)
        # Note: Your Image model does NOT have a 'user' field, so we omit it.
        new_image = Image.objects.create(
            file=file_obj,
            image_name=file_obj.name 
        )

        # 3. Create the ProductImage link
        product_image = ProductImage.objects.create(
            image=new_image,
            **validated_data
        )
        return product_image

# class ProductVideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVideo
#         fields = '__all__'
# ... keep your existing imports ...

class ProductVideoSerializer(serializers.ModelSerializer):
    # Read-only field to show the URL
    video_url = serializers.FileField(source='video_file', read_only=True)
    
    # Write-only field for the upload
    file_upload = serializers.FileField(source='video_file', write_only=True)

    class Meta:
        model = ProductVideo
        fields = ['id', 'video_url', 'file_upload', 'title', 'description', 'created_at']
        read_only_fields = ['product', 'created_at']

# ... keep the rest of the file ...
# -----------------------------
# Variant Serializer (THE FIX IS HERE)
# -----------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    # 1. READ ONLY: 'attributes' shows the rich data (Name: Red, Hex: #FF0000)
    attributes = VariationOptionSerializer(source='variation_options', many=True, read_only=True)
    
    # 2. WRITE ONLY: 'variation_option_ids' accepts the list of IDs (e.g., [1])
    # We use source='variation_options' so it maps automatically to the model field
    variation_option_ids = serializers.PrimaryKeyRelatedField(
        queryset=VariationOption.objects.all(),
        source='variation_options',
        many=True,
        write_only=True
    )

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'price', 'stock_qty', 'attributes', 'variation_option_ids']


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
    category_details = CategorySerializer(source='category', read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)
    
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'short_description', 'description',
            'status', 'featured', 'trending',
            'category', 'category_details',
            'brand', 'brand_details',
            'weight_name', 'weight_value',
            'price_range', 
            'variants', 
            'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vendor_shop', 'status', 'created_at', 'updated_at', 'slug']

    def get_price_range(self, obj):
        variants = obj.variants.all()
        if not variants:
            return "N/A"
        prices = [v.price for v in variants]
        min_p = min(prices)
        max_p = max(prices)
        if min_p == max_p:
            return f"{min_p}"
        return f"{min_p} - {max_p}"

    def create(self, validated_data):
        if 'slug' not in validated_data:
            validated_data['slug'] = slugify(validated_data['product_name'])
            original_slug = validated_data['slug']
            counter = 1
            while Product.objects.filter(slug=validated_data['slug']).exists():
                validated_data['slug'] = f"{original_slug}-{counter}"
                counter += 1
        return super().create(validated_data)