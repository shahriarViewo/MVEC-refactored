from rest_framework import serializers
from .models import Order, VendorOrder, OrderItem
from products.serializers import ProductVariantSerializer
from vendors.serializers import VendorShopSerializer

# -----------------------------
# Order Item Serializer
# -----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    # Read-only product details for history display
    variant_details = ProductVariantSerializer(source='product_variant', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'variant_details', 'quantity', 'price']


# -----------------------------
# Vendor Order Serializer
# -----------------------------
class VendorOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shop_details = VendorShopSerializer(source='vendor_shop', read_only=True)

    class Meta:
        model = VendorOrder
        fields = ['id', 'order', 'vendor_shop', 'shop_details', 'subtotal', 'status', 'items', 'created_at']


# -----------------------------
# Main Order Serializer (Customer View)
# -----------------------------
class OrderSerializer(serializers.ModelSerializer):
    # Nested vendor orders allow customer to see "Package 1 from Shop A", "Package 2 from Shop B"
    vendor_orders = VendorOrderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'vendor_orders', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']


# -----------------------------
# Checkout Action Serializer (Input Only)
# -----------------------------
class CheckoutItemSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CheckoutSerializer(serializers.Serializer):
    """
    Receives a simple list of items.
    The View logic handles:
    1. Grouping items by Vendor
    2. Creating the Parent Order
    3. Creating VendorOrders
    4. Creating OrderItems
    """
    items = CheckoutItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    # Add address_id here if needed