from django.contrib import admin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import VendorApplication, Vendor


class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "store_name", "status", "created_at")
    list_filter = ("status",)
    actions = ["approve_vendor", "reject_vendor"]

    # APPROVE VENDOR
    def approve_vendor(self, request, queryset):
        for application in queryset:
            if application.status == "approved":
                continue

            # Generate secret key here (admin only)
            secret_key = get_random_string(10).upper()
            hashed_secret_key = make_password(secret_key)

            # Create vendor
            vendor = Vendor.objects.create(
                user=application.user,
                store_name=application.store_name,
                address=application.address,
                phone=application.phone,
                vendor_secret_key=hashed_secret_key
            )

            # Update application status
            application.status = "approved"
            application.save()

            user_display = (
                application.user.get_full_name() or "User"
            )

            # Send email
            subject = "Your Vendor Account is Approved"
            message = f"""
                Dear {user_display},

                Congratulations! Your vendor application for "{application.store_name}" has been approved.

                Vendor ID: {vendor.vendor_id}
                Vendor Secret Key: {secret_key}

                Please login first as a normal user, then access the vendor dashboard using your Vendor ID and Secret Key.

                Best regards,
                Shopora Team
                """
            send_mail(subject, message, None, [
                      application.user.email], fail_silently=False)

    approve_vendor.short_description = "Approve selected vendor applications"

    # REJECT VENDOR
    def reject_vendor(self, request, queryset):
        for application in queryset:
            if application.status == "rejected":
                continue
            Vendor.objects.filter(user=application.user).delete()
            application.status = "rejected"
            application.save()

            user_display = (
                application.user.get_full_name() or "User"
            )

            # Send rejection email
            subject = "Your Vendor Application was Rejected"
            message = f"""
                Dear {user_display},

                We regret to inform you that your vendor application for "{application.store_name}" has been rejected.

                You may contact support for further details.

                Best regards,
                Shopora Team
                """
            send_mail(subject, message, None, [
                      application.user.email], fail_silently=False)

    reject_vendor.short_description = "Reject selected vendor applications"

    # HANDLE STATUS CHANGE IN ADMIN EDIT
    def save_model(self, request, obj, form, change):
        if change:
            old = VendorApplication.objects.get(pk=obj.pk)
            if old.status == "approved" and obj.status == "rejected":
                Vendor.objects.filter(user=obj.user).delete()
        super().save_model(request, obj, form, change)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_id', 'user', 'store_name')


admin.site.register(VendorApplication, VendorApplicationAdmin)
admin.site.register(Vendor, VendorAdmin)
