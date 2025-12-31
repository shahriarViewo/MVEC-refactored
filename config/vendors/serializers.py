from rest_framework import serializers
from .models import VendorShop
from accounts.models import Image
from accounts.serializers import ImageSerializer, UserSerializer

class VendorShopSerializer(serializers.ModelSerializer):
    # Read-only nested representations for display
    logo_details = ImageSerializer(source='logo_image', read_only=True)
    banner_details = ImageSerializer(source='banner_image', read_only=True)
    vendor_details = UserSerializer(source='vendor', read_only=True)

    # Write-only ID fields for updates
    logo_image_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source='logo_image', write_only=True, required=False, allow_null=True
    )
    banner_image_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source='banner_image', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = VendorShop
        fields = [
            'id', 
            'vendor_details', 
            'shopname', 
            'slug', 
            'shop_email', 
            'contact', 
            'description', 
            'location', 
            'status', 
            'logo_details', 
            'logo_image_id',
            'banner_details', 
            'banner_image_id',
            'created_at'
        ]
        # Sensitive fields that general public or vendor shouldn't touch directly via this serializer
        read_only_fields = ['vendor', 'total_sell', 'created_at']

# -----------------------------
# Admin Serializer (For Approvals & Commission)
# -----------------------------
class AdminVendorShopSerializer(VendorShopSerializer):
    class Meta(VendorShopSerializer.Meta):
        fields = VendorShopSerializer.Meta.fields + [
            'is_approved', 
            'approved_at', 
            'sell_commission_percentage', 
            'product_tax_percent', 
            'product_vat_percent'
        ]