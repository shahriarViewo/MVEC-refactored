from django.db import models
from accounts.models import Image
# Dynamic import is usually preferred in models via string, 
# but for clarity in this file context:
# We reference 'vendors.VendorShop' via string to avoid circular imports.

# -----------------------------
# Brand
# -----------------------------
class Brand(models.Model):
    # Null vendor_shop means it's a "Global" brand (managed by Admin)
    # If set, it's a private brand for that specific vendor
    vendor_shop = models.ForeignKey(
        'vendors.VendorShop', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    is_global = models.BooleanField(default=False)
    brand_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=255) # Could be integer for sorting, keeping Char as per your DB
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['vendor_shop']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return self.brand_name


# -----------------------------
# Category
# -----------------------------
class Category(models.Model):
    parent_category = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='subcategories'
    )
    category_name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True) # Icon class or URL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['parent_category']),
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


# -----------------------------
# Variation (e.g., Color, Size)
# -----------------------------
# class Variation(models.Model):
#     vendor_shop = models.ForeignKey(
#         'vendors.VendorShop', 
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True
#     )
#     is_global = models.BooleanField(default=False)
#     name = models.CharField(max_length=255) # e.g., "Size", "Material"
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
class Variation(models.Model):
    # NEW: Define how this option should look on the frontend
    DISPLAY_MODE_CHOICES = [
        ('text', 'Text (Buttons)'),
        ('color', 'Color (Hex Code)'),
        ('image', 'Image (Pattern/Texture)'),
    ]

    vendor_shop = models.ForeignKey(
        'vendors.VendorShop', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    is_global = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    
    # NEW: Field added
    display_mode = models.CharField(
        max_length=10, 
        choices=DISPLAY_MODE_CHOICES, 
        default='text'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_display_mode_display()})"

# -----------------------------
# Variation Options
# -----------------------------
# class VariationOption(models.Model):
#     variation = models.ForeignKey(
#         Variation, 
#         on_delete=models.CASCADE, 
#         related_name='options'
#     )
#     value = models.CharField(max_length=255) # e.g., "Red", "XL"
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.variation.name}: {self.value}"

class VariationOption(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=255)
    
    # NEW: Fields added for the visual data
    color_code = models.CharField(max_length=7, null=True, blank=True, help_text="Hex code (e.g. #FF0000)")
    pattern_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variation.name}: {self.value}"