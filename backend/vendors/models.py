from django.db import models
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password
from accounts.models import User
import uuid


class VendorApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.store_name} ({self.status})"


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_id = models.CharField(max_length=20, unique=True, editable=False)
    vendor_secret_key = models.CharField(
        max_length=128, editable=False)  # hashed
    store_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---------------------------
    # Save method for vendor_id and slug only
    # ---------------------------
    def save(self, *args, **kwargs):
        # Auto-generate vendor_id if not exists
        if not self.vendor_id:
            while True:
                vid = f"VND-{uuid.uuid4().hex[:8].upper()}"
                if not Vendor.objects.filter(vendor_id=vid).exists():
                    self.vendor_id = vid
                    break

        # Auto-generate slug
        if not self.slug:
            base_slug = slugify(self.store_name)
            slug = base_slug
            count = 1
            while Vendor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.vendor_id
