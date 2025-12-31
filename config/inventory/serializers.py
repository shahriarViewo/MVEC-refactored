from rest_framework import serializers
from django.db import transaction
from .models import StockMovement
# We need to import the actual model here to update it
from products.models import ProductVariant 

# -----------------------------
# Read-Only History Serializer
# -----------------------------
class StockMovementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'variant', 'created_by', 'created_by_name', 
            'movement_type', 'quantity_change', 'balance_after', 
            'remarks', 'created_at'
        ]
        read_only_fields = ['balance_after', 'created_at']


# -----------------------------
# Stock Update Action Serializer
# -----------------------------
class InventoryAdjustmentSerializer(serializers.Serializer):
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(), source='variant'
    )
    quantity = serializers.IntegerField()
    type = serializers.ChoiceField(choices=StockMovement.MOVEMENT_TYPE_CHOICES)
    remarks = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        variant = validated_data['variant']
        qty = validated_data['quantity']
        move_type = validated_data['type']
        user = self.context['request'].user if 'request' in self.context else None

        # Determine sign based on type if the user just sends a positive number
        # (Logic can be customized, here we assume the API sends strict +/- or we enforce it)
        # For simplicity, let's assume 'quantity' input handles the sign, 
        # OR we enforce logic: Restock = +, Order = -
        
        # Enforce logic for safety:
        if move_type in ['order', 'damage'] and qty > 0:
            qty = -qty
        
        with transaction.atomic():
            # Lock row for update
            variant_obj = ProductVariant.objects.select_for_update().get(pk=variant.pk)
            
            # Update generic stock field in Products App
            variant_obj.stock_qty += qty
            variant_obj.save()

            # Create Log
            movement = StockMovement.objects.create(
                variant=variant_obj,
                created_by=user,
                movement_type=move_type,
                quantity_change=qty,
                balance_after=variant_obj.stock_qty,
                remarks=validated_data.get('remarks', '')
            )
        
        return movement