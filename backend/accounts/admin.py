from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ("email", "username", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")

    readonly_fields = ("created_at", "updated_at")  # IMPORTANT FIX

    fieldsets = (
        (None, {"fields": ("email", "username",
         "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_staff",
         "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),  # NOW ALLOWED
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
