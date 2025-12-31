from django.contrib import admin
from .models import VendorShop

@admin.register(VendorShop)
class VendorShopAdmin(admin.ModelAdmin):
    # Corrected field names based on your models.py
    list_display = ['shopname', 'vendor', 'status', 'is_approved']
    
    # Corrected filters
    list_filter = ['status', 'is_approved']
    
    # 'vendor' is a relationship to User, so we search by vendor's email
    search_fields = ['shopname', 'vendor__email']