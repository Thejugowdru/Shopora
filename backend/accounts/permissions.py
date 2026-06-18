from rest_framework.permissions import BasePermission


class IsAdminGroup(BasePermission):
    # Custom message instead of the generic permission denied message
    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_admin
        )


class IsVendorGroup(BasePermission):
    message = "Vendor account required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_vendor
        )
