from django.contrib import admin
from django.utils.crypto import get_random_string

from .models import VendorApplication, Vendor


class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "store_name", "status", "created_at")
    list_filter = ("status",)
    actions = ["approve_vendor", "reject_vendor"]

    # ADMIN ACTION → APPROVE
    def approve_vendor(self, request, queryset):
        for application in queryset:
            if application.status == "approved":
                continue

            vendor_id = "VEN" + get_random_string(6).upper()
            temp_password = get_random_string(10)

            # Set temp password for the user
            application.user.set_password(temp_password)
            application.user.save()

            # Create vendor
            Vendor.objects.create(
                user=application.user,
                store_name=application.store_name,
                address=application.address,
                gstin=application.gstin,
                phone=application.phone,
                document=application.document,
                vendor_id=vendor_id,
            )

            application.status = "approved"
            application.save()

            self.message_user(
                request,
                f"Vendor created: {vendor_id} | Password: {temp_password}"
            )

    approve_vendor.short_description = "Approve selected vendor applications"

    # ADMIN ACTION → REJECT
    def reject_vendor(self, request, queryset):
        for application in queryset:
            # delete vendor if exists
            Vendor.objects.filter(user=application.user).delete()

        queryset.update(status="rejected")
        self.message_user(request, "Vendor(s) rejected and accounts deleted.")

    reject_vendor.short_description = "Reject selected vendor applications"

    # HANDLE STATUS CHANGE FROM ADMIN EDIT PAGE
    def save_model(self, request, obj, form, change):
        """
        If admin edits the entry manually and changes status to rejected,
        delete Vendor automatically.
        """
        if change:
            old = VendorApplication.objects.get(pk=obj.pk)

            # status changed from approved → rejected
            if old.status == "approved" and obj.status == "rejected":
                Vendor.objects.filter(user=obj.user).delete()

        super().save_model(request, obj, form, change)


admin.site.register(VendorApplication, VendorApplicationAdmin)

admin.site.register(Vendor)
