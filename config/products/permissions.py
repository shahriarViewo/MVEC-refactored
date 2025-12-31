from rest_framework import permissions

class IsVendorOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a product (Vendor) to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the shop
        # Check if the user has a vendor_shop profile and it matches the product's shop
        return hasattr(request.user, 'vendor_shop') and obj.vendor_shop == request.user.vendor_shop