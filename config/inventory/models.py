from django.db import models
from django.conf import settings
# We reference ProductVariant via string to avoid circular imports if products imports inventory later
# But strictly, products depends on nothing usually. 
# Here we use lazy loading just in case.

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('initial', 'Initial Stock'),
        ('restock', 'Restock (Vendor Add)'),
        ('order', 'Order Deduction'),
        ('cancel', 'Order Cancellation (Restock)'),
        ('correction', 'Manual Correction'),
        ('return', 'Customer Return'),
        ('damage', 'Damaged/Lost'),
    ]

    # The specific SKU being adjusted
    variant = models.ForeignKey(
        'products.ProductVariant', 
        on_delete=models.CASCADE, 
        related_name='stock_movements'
    )
    
    # Who made the change (Vendor, Admin, or System/None for automated orders)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity_change = models.IntegerField(help_text="Positive for addition, negative for deduction")
    
    # Snapshot of stock after this specific movement (useful for auditing)
    balance_after = models.IntegerField(null=True, blank=True) 
    
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['variant']),
            models.Index(fields=['movement_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.variant.sku}: {self.quantity_change} ({self.movement_type})"