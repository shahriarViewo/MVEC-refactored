from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    
    # Optional: Allow users to upload an image with their review
    image = models.ForeignKey(
        'accounts.Image', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    is_verified_purchase = models.BooleanField(default=False)
    status = models.BooleanField(default=True) # Admin/Vendor can hide if inappropriate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product') # Usually one review per product per user
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.rating}* - {self.product.product_name}"


class VendorReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor_shop = models.ForeignKey('vendors.VendorShop', on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'vendor_shop')
        indexes = [
            models.Index(fields=['vendor_shop']),
        ]

    def __str__(self):
        return f"{self.rating}* - {self.vendor_shop.shopname}"