from django.contrib import admin
from .models import Product, ProductVariant, ProductImage

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    show_change_link = True
    fields = ['sku', 'price', 'stock_qty']
    # We don't inline 'variation_options' because ManyToMany is hard to edit inline

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'vendor_shop', 'status', 'category', 'updated_at']
    list_filter = ['status', 'trending', 'featured']
    search_fields = ['product_name', 'vendor_shop__shopname']
    inlines = [ProductVariantInline, ProductImageInline]
    
    # Action to bulk-approve products 
    actions = ['make_published', 'make_rejected']

    def make_published(self, request, queryset):
        queryset.update(status='active')
    make_published.short_description = "Mark selected products as Published (Active)"

    def make_rejected(self, request, queryset):
        queryset.update(status='rejected')
    make_rejected.short_description = "Reject selected products"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['sku', 'product', 'price', 'stock_qty']
    search_fields = ['sku', 'product__product_name']