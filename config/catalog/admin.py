from django.contrib import admin
from .models import Category, Brand, Variation, VariationOption

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'parent_category', 'id']
    search_fields = ['category_name']
    list_filter = ['parent_category']
    # Start with global categories (Parent=Null)
    ordering = ['parent_category', 'category_name'] 

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'is_global', 'vendor_shop']
    list_filter = ['is_global', 'vendor_shop']
    search_fields = ['brand_name']

class VariationOptionInline(admin.TabularInline):
    model = VariationOption
    extra = 1
    # Show the visual fields in the inline editor [cite: 34, 35]
    fields = ['value', 'color_code', 'pattern_image']

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_mode', 'is_global', 'vendor_shop']
    list_filter = ['display_mode', 'is_global']
    inlines = [VariationOptionInline]
    
    # Helper to see what mode is selected [cite: 31]
    fieldsets = (
        (None, {
            'fields': ('name', 'display_mode', 'is_global', 'vendor_shop')
        }),
    )