from django.db import models
from django.conf import settings # Best practice to reference User model
# We assume 'accounts' app is installed
from accounts.models import Image 

class VendorShop(models.Model):
    # One user can own exactly one shop (common in MVP multivendor setups)
    vendor = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='vendor_shop'
    )
    logo_image = models.ForeignKey(
        Image, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='logo_shops'
    )
    banner_image = models.ForeignKey(
        Image, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='banner_shops'
    )
    shopname = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    shop_email = models.EmailField(unique=True)
    contact = models.CharField(max_length=30, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    
    # Status & Approval
    status = models.BooleanField(default=True) # Vendor can toggle their shop visibility
    is_approved = models.BooleanField(default=False) # Admin controls this
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Financial Settings (Vendor Specific Overrides)
    sell_commission_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_tax_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_vat_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Metrics
    total_sell = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['vendor']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.shopname