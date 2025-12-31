from rest_framework import serializers
from .models import ProductReview, VendorReview
from accounts.serializers import UserSerializer, ImageSerializer

# -----------------------------
# Product Review Serializer
# -----------------------------
class ProductReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    image_details = ImageSerializer(source='image', read_only=True)
    
    # Write-only field for image upload ID
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=None, # Set dynamically or via import if needed
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
        # 'user' is set from request.user
        # 'is_verified_purchase' is calculated by backend checking Orders

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from accounts.models import Image
            self.fields['image_id'].queryset = Image.objects.all()
        except ImportError:
            pass


# -----------------------------
# Vendor Review Serializer
# -----------------------------
class VendorReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = VendorReview
        fields = ['id', 'user_details', 'vendor_shop', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']