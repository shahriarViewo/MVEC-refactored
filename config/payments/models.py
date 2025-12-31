from django.db import models
# Reference 'vendors.VendorShop' via string to avoid circular imports

class VendorWallet(models.Model):
    vendor_shop = models.OneToOneField(
        'vendors.VendorShop', 
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet: {self.vendor_shop.shopname}"


class VendorTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'), # Money coming in (Sale)
        ('debit', 'Debit')    # Money going out (Payout or Refund)
    ]

    wallet = models.ForeignKey(
        VendorWallet, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(null=True, blank=True) # e.g., "Sale of Order #123"
    
    # Immutable log usually, but updated_at provided for consistency
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type.upper()} {self.amount} - {self.wallet.vendor_shop.shopname}"


class VendorPayout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    wallet = models.ForeignKey(VendorWallet, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payout_date = models.DateTimeField(null=True, blank=True) # Date actually paid
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin note for rejection or transaction ID from bank
    admin_note = models.TextField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payout {self.amount} ({self.status})"