from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'vendor',
        'category',
        'price',
        'stock',
        'is_active',
        'is_approved',
        'created_at'
    )

    list_filter = ('is_approved', 'is_active', 'category')
    search_fields = ('name', 'vendor__user__email')
    readonly_fields = ('created_at', 'updated_at')

    actions = ('approve_products', 'disapprove_products')

    # ✅ APPROVE PRODUCTS
    def approve_products(self, request, queryset):
        approved_count = 0

        for product in queryset:
            if product.is_approved:
                continue

            product.is_approved = True
            product.save()

            subject = "🎉 Your product has been approved"
            message = f"""
                Hello {product.vendor.user.get_full_name() or product.vendor.user.username},

                Your product "{product.name}" has been APPROVED
                and is now live on our platform.

                Category: {product.category}
                Price: ₹{product.price}

                Thank you,
                ThejuSphere Team
                """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [product.vendor.user.email],
                fail_silently=False
            )

            approved_count += 1

        self.message_user(
            request,
            f"{approved_count} product(s) approved and email sent."
        )

    approve_products.short_description = "Approve selected products"

    # ❌ DISAPPROVE PRODUCTS

    def disapprove_products(self, request, queryset):
        disapproved_count = 0

        for product in queryset:
            if not product.is_approved:
                continue

            product.is_approved = False
            product.save()

            subject = "❌ Your product has been disapproved"
            message = f"""
                Hello {product.vendor.user.get_full_name() or product.vendor.user.username},

                Your product "{product.name}" has been DISAPPROVED.

                Please review the product details and submit again.

                Thank you,
                ThejuSphere Team
                """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [product.vendor.user.email],
                fail_silently=False
            )

            disapproved_count += 1

        self.message_user(
            request,
            f"{disapproved_count} product(s) disapproved and email sent."
        )

    disapprove_products.short_description = "Disapprove selected products"
