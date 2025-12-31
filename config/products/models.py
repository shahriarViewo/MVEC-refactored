from django.db import models
from accounts.models import Image
from vendors.models import VendorShop
from catalog.models import Category, Brand, VariationOption

# -----------------------------
# Product (Parent)
# -----------------------------
class Product(models.Model):
    # STATUS_CHOICES = [
    #     ('active', 'Active'),
    #     ('inactive', 'Inactive'),
    #     ('published', 'Published'),
    #     ('pending', 'Pending')
    # ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('active', 'Active (Published)'),
        ('inactive', 'Inactive (Hidden)'),
        ('rejected', 'Rejected'),
    ]

    WEIGHT_CHOICES = [('gm', 'gm'), ('kg', 'kg'), ('lb', 'lb')]

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    vendor_shop = models.ForeignKey(VendorShop, on_delete=models.CASCADE, related_name='products')
    
    # Content
    product_name = models.CharField(max_length=255)
    short_description = models.TextField()
    description = models.TextField()
    slug = models.SlugField()
    
    # Marketing Flags
    trending = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Physical Dimensions (Global Defaults for the product)
    weight_name = models.CharField(max_length=2, choices=WEIGHT_CHOICES, null=True, blank=True)
    weight_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    is_virtual = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('vendor_shop', 'slug')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['featured']),
            models.Index(fields=['trending']),
        ]

    def __str__(self):
        return self.product_name


# -----------------------------
# Product Variants (SKUs)
# -----------------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField() # Note: Logic might move to Inventory app, but field stays here for simple lookups
    variation_options = models.ManyToManyField(VariationOption, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'sku')
        indexes = [
            models.Index(fields=['sku']),
        ]

    def __str__(self):
        return f"{self.product.product_name} - {self.sku}"


# -----------------------------
# Media (Images & Videos)
# -----------------------------
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    
    # NEW: Link this image to a specific variant (Optional)
    variant = models.ForeignKey(
        'ProductVariant', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='variant_specific_images'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='product_videos/')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------------------
# SEO
# -----------------------------
class ProductSEOConfig(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seo_config')
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    canonical_url = models.CharField(max_length=255, null=True, blank=True)
    tags = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# -----------------------------
# Downloadable (Digital)
# -----------------------------
class DownloadableProduct(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='downloads')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='digital_products/')
    description = models.TextField(null=True, blank=True)
    secret_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)