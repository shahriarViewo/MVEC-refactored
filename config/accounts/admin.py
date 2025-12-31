from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

# Define a custom Admin class to display your new fields (User Type, Vendor status)
class CustomUserAdmin(UserAdmin):
    model = User
    # Display these columns in the list view
    list_display = ['email', 'username', 'user_type', 'is_vendor', 'is_staff', 'is_active']
    
    # Add filters for quick searching
    list_filter = ['user_type', 'is_vendor', 'is_staff', 'is_active']
    
    # Organize the "Edit User" form to include your custom fields
    fieldsets = UserAdmin.fieldsets + (
        ('Nissin Custom Fields', {'fields': ('user_type', 'is_vendor', 'is_vendor_approved', 'phone_no')}),
    )
    # Note: 'phone_no' is in Profile usually, but if you moved it to User, add it here. 
    # Based on your previous model, phone_no was in UserProfile, so remove 'phone_no' above if it's not in User.
    # Corrected fieldset based on your database.txt models:
    fieldsets = UserAdmin.fieldsets + (
        ('Nissin Custom Fields', {'fields': ('user_type', 'is_vendor', 'is_vendor_approved')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)