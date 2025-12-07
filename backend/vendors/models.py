from django.contrib.auth.hashers import make_password
from django.db import models
from accounts.models import User

# Create your models here.


class VendorApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    address = models.TextField()
    gstin = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20)
    document = models.FileField(
        upload_to='vendor_docs/', null=True, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.store_name} ({self.status})"


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_id = models.CharField(max_length=20, unique=True)
    store_name = models.CharField(max_length=255)
    address = models.TextField()
    gstin = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20)
    document = models.FileField(
        upload_to='vendor_docs/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_id
