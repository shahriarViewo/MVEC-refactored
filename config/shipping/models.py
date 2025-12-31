from django.db import models
# Reference 'vendors.VendorShop' via string to avoid circular imports

class ShippingRate(models.Model):
    METHOD_CHOICES = [('Standard', 'Standard'), ('Express', 'Express')]
    
    # If null, it's a default platform rate. If set, it belongs to a specific vendor.
    vendor_shop = models.ForeignKey(
        'vendors.VendorShop', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='shipping_rates'
    )
    is_platform_rate = models.BooleanField(default=True)
    
    shipping_class = models.CharField(max_length=255) # e.g. "Heavy Items", "Lightweight"
    country = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    delivery_time = models.CharField(max_length=255) # e.g. "3-5 Business Days"
    
    free_shipping_min_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def_country_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = "Global" if self.is_platform_rate else "Vendor"
        return f"{self.shipping_class} - {self.country} ({owner})"


class WeightCostRule(models.Model):
    SHIPPING_METHOD_CHOICES = [('per_unit', 'Per Unit'), ('rules', 'Rules')]
    
    shipping_rate = models.ForeignKey(ShippingRate, on_delete=models.CASCADE, related_name='cost_rules')
    
    # Geographic granularities (optional overrides)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    
    shipping_calculation_method = models.CharField(
        max_length=10, 
        choices=SHIPPING_METHOD_CHOICES, 
        default='per_unit'
    )
    
    # If per_unit, use this:
    per_unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Fallback cost if rules don't match
    default_rule_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WeightCostRuleItem(models.Model):
    # Defines the tiers (e.g., 0-5kg = $10)
    weight_cost_rule = models.ForeignKey(WeightCostRule, on_delete=models.CASCADE, related_name='rule_items')
    weight = models.DecimalField(max_digits=10, decimal_places=2) # Upper limit for this tier
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)