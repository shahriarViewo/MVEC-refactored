from django.db import models
from django.conf import settings
# Lazy imports for relations
# 'vendors.VendorShop', 'products.ProductVariant'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # The Customer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Financials (Grand Total of all sub-orders)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Overall Status (Simple aggregation, or main status)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Address Snapshot (Optional but recommended to store copy of address at time of order)
    # For now, adhering to your list, we assume it might link to UserProfile or be a snapshot JSON/Text
    # If using Address ID, be careful if user edits address later.
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class VendorOrder(models.Model):
    # The "Split" Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='vendor_orders')
    vendor_shop = models.ForeignKey('vendors.VendorShop', on_delete=models.CASCADE, related_name='orders')
    
    # Financials for this specific vendor
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Status specific to this vendor's shipment
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SubOrder #{self.id} (Ref Order #{self.order.id})"


class OrderItem(models.Model):
    vendor_order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at moment of purchase
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.product_variant.sku} x {self.quantity}"