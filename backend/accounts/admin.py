from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    fields = ('id', 'username', 'email', 'groups',
              'is_active', 'is_staff', 'is_superuser')


admin.site.register(User, UserAdmin)
