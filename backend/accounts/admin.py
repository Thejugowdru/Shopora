from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address, UserSearchHistory


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "display_name",
        "group",
        "email_verified",
        "temp_password",
        "is_active",
        "is_staff",
        "created_at"
    )

    list_filter = (
        "group",
        "email_verified",
        "temp_password",
        "is_active",
        "is_staff"
    )

    search_fields = (
        "email",
        "display_name"
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "email",
                    "password",
                    "display_name",
                    "group"
                )
            }
        ),
        (
            "Status",
            {
                "fields": (
                    "email_verified",
                    "temp_password",
                    "is_active",
                    "is_staff",
                    "is_superuser"
                )
            }
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at"
                )
            }
        )
    )

    readonly_fields = (
        "created_at",
        "updated_at"
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "phone",
        "city",
        "state",
        "pincode",
        "address_type",
        "is_default"
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "pincode",
        "user__email"
    )

    list_filter = (
        "address_type",
        "is_default",
        "state"
    )

    ordering = ("-created_at",)


@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "search_text",
        "item_count",
        "searched_at"
    )

    search_fields = (
        "user__email",
        "search_text"
    )

    ordering = ("-searched_at",)

    readonly_fields = (
        "user",
        "search_text",
        "item_count",
        "searched_at"
    )
