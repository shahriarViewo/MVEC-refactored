from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('super_admin', 'Super Admin'),
    ]
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    remember_token = models.CharField(max_length=100, null=True, blank=True)

    # Vendor specific flags
    is_vendor = models.BooleanField(default=False)
    is_vendor_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fname', 'lname']

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.email


# -----------------------------
# Global Image Model 
# (Placed here as a dependency for Profiles)
# -----------------------------
class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.image_name and self.file:
            self.image_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.image_name


# -----------------------------
# Address
# -----------------------------
class Address(models.Model):
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city}, {self.country}"


# -----------------------------
# User Profile
# -----------------------------
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    phone_no = models.CharField(max_length=255)
    website = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    def_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"


# -----------------------------
# Vendor Staff
# -----------------------------
class VendorStaff(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('editor', 'Editor'),
        ('staff', 'Staff'),
    ]
    # Using string reference to avoid circular import with 'vendors' app
    vendor_shop = models.ForeignKey('vendors.VendorShop', on_delete=models.CASCADE, related_name='staff_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"