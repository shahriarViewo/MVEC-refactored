from rest_framework import serializers
from .models import ShippingRate, WeightCostRule, WeightCostRuleItem

# -----------------------------
# Rule Items (The Tiers)
# -----------------------------
class WeightCostRuleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightCostRuleItem
        fields = ['id', 'weight', 'cost']


# -----------------------------
# Cost Rules (The Strategy)
# -----------------------------
class WeightCostRuleSerializer(serializers.ModelSerializer):
    rule_items = WeightCostRuleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = WeightCostRule
        fields = [
            'id', 'state', 'city', 'shipping_calculation_method', 
            'per_unit_cost', 'default_rule_cost', 'rule_items'
        ]


# -----------------------------
# Main Shipping Rate Serializer
# -----------------------------
class ShippingRateSerializer(serializers.ModelSerializer):
    cost_rules = WeightCostRuleSerializer(many=True, read_only=True)

    class Meta:
        model = ShippingRate
        fields = [
            'id', 'vendor_shop', 'is_platform_rate', 'shipping_class', 
            'country', 'method', 'delivery_time', 
            'free_shipping_min_order', 'def_country_price', 
            'status', 'cost_rules'
        ]
        read_only_fields = ['vendor_shop'] 
        # Vendor ID usually injected by view to prevent users creating rules for others