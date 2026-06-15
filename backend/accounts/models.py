from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.validators import RegexValidator


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("display_name", "Super Admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        admin_group = Group.objects.get(name="ADMIN")
        user = self.create_user(
            email=email, password=password, group=admin_group, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255)

    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, related_name="shopora_users")

    email_verified = models.BooleanField(default=False)

    temp_password = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def role(self):
        return self.group.name

    @property
    def is_customer(self):
        return self.group.name == "CUSTOMER"

    @property
    def is_vendor(self):
        return self.group.name == "VENDOR"

    @property
    def is_admin(self):
        return self.group.name == "ADMIN"

    @property
    def is_shopora_support(self):
        return self.group.name == "SHOPORA SUPPORT"

    @property
    def is_shopora_operations(self):
        return self.group.name == "SHOPORA OPERATIONS"


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('HOME', 'Home'),
        ('OFFICE', 'Office'),
        ('OTHER', 'Other')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=200)

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Enter valid mobile number"
            )
        ]
    )

    building = models.CharField(max_length=100, null=True, blank=True)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    address_type = models.CharField(
        max_length=10, choices=ADDRESS_TYPE_CHOICES, default='HOME')

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "full_name", "address_line1", "pincode"],
                name="unique_user_address"
            )
        ]

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(
                pk=self.pk
            ).update(is_default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class UserSearchHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="search_history"
    )

    search_text = models.CharField(max_length=255)
    item_count = models.PositiveIntegerField(default=0)

    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self):
        return f"{self.user.email} - {self.search_text}"
