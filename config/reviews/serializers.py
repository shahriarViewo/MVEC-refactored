from rest_framework import serializers
from .models import ProductReview, VendorReview
from accounts.serializers import UserSerializer, ImageSerializer
from accounts.models import Image
# -----------------------------
# Product Review Serializer
# -----------------------------
class ProductReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    image_details = ImageSerializer(source='image', read_only=True)
    
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        source='image', 
        write_only=True, 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = ProductReview
        fields = [
            'id', 'user_details', 'product', 'rating', 'comment', 
            'image_details', 'image_id', 'is_verified_purchase', 'created_at'
        ]
        read_only_fields = ['user', 'is_verified_purchase', 'created_at']
# -----------------------------
# Vendor Review Serializer
# -----------------------------
class VendorReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = VendorReview
        fields = ['id', 'user_details', 'vendor_shop', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']