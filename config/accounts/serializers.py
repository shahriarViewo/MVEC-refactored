from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, Address, Image, VendorStaff

User = get_user_model()

# -----------------------------
# Image Serializer
# -----------------------------
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file', 'image_name', 'created_at']
        read_only_fields = ['image_name', 'created_at']


# -----------------------------
# Address Serializer
# -----------------------------
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# -----------------------------
# User Serializer (Basic info)
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'fname', 'lname', 'user_type', 'is_vendor', 'is_vendor_approved']
        read_only_fields = ['is_vendor', 'is_vendor_approved', 'user_type']


# -----------------------------
# User Registration Serializer
# -----------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'fname', 'lname', 'password', 'user_type']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -----------------------------
# User Profile Serializer
# -----------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = ImageSerializer(read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source='image', write_only=True, required=False
    )
    def_address = AddressSerializer(read_only=True)
    def_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source='def_address', write_only=True, required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone_no', 'website', 'gender', 'date_of_birth', 
            'image', 'image_id', 'def_address', 'def_address_id', 
            'created_at', 'updated_at'
        ]


# -----------------------------
# Vendor Staff Serializer
# -----------------------------
class VendorStaffSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    
    # We use PrimaryKeyRelatedField for the shop to handle the relationship via ID
    vendor_shop_id = serializers.PrimaryKeyRelatedField(
        queryset=None, # Needs to be set dynamically in view or imports if possible, 
                       # but standard practice for decoupled apps is checking ID validity in view or loosely here.
                       # For strict typing, we would import VendorShop, but that causes circular import.
                       # We will set queryset in the __init__ or handle at View level.
        read_only=False
    )

    class Meta:
        model = VendorStaff
        fields = ['id', 'vendor_shop_id', 'user_details', 'user_id', 'role', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic import to break circular dependency in serializers
        try:
            from vendors.models import VendorShop
            self.fields['vendor_shop_id'].queryset = VendorShop.objects.all()
        except ImportError:
            pass