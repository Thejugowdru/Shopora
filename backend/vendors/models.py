from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# Create your models here.
class VendorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="vendor_profile"
    )

    business_name = models.CharField(max_length=300)
    business_description = models.TextField(blank=True, null=True)

    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)

    support_email = models.EmailField()
    support_phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Enter a valid 10-digit mobile number.'
            )
        ]
    )

    business_address = models.TextField()

    store_slug = models.SlugField(max_length=255, unique=True)

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ],
        null=True,
        blank=True
    )

    kyc_documents_uploaded = models.BooleanField(default=False, db_index=True)
    kyc_verified = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.business_name


class VendorKYC(models.Model):
    gst_validator = RegexValidator(
        regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
        message='Enter a valid GSTIN.'
    )
    pan_validator = RegexValidator(
        regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
        message="Enter a valid PAN"
    )
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    vendor = models.OneToOneField(
        VendorProfile, on_delete=models.CASCADE, related_name="vendor_kyc")

    gst_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[gst_validator],
    )
    pan_number = models.CharField(
        max_length=10, unique=True, validators=[pan_validator])

    gst_document = models.FileField(upload_to="gst_documents/")
    pan_document = models.FileField(upload_to="pan_documents/")

    verification_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING", db_index=True)

    remarks = models.TextField(blank=True, null=True)

    verified_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="verified_vendor_kycs",
        null=True,
        blank=True
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.business_name} KYC"


class VendorPreviousKYC(models.Model):
    gst_validator = RegexValidator(
        regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
        message='Enter a valid GSTIN.'
    )
    pan_validator = RegexValidator(
        regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
        message="Enter a valid PAN"
    )
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    vendor = models.ForeignKey(
        VendorProfile, on_delete=models.CASCADE, related_name="previous_kycs")

    gst_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[gst_validator],
    )
    pan_number = models.CharField(
        max_length=10, unique=True, validators=[pan_validator])

    gst_document = models.FileField(upload_to="gst_previous_documents/")
    pan_document = models.FileField(upload_to="pan_previous_documents/")

    verification_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING", db_index=True)

    remarks = models.TextField(blank=True, null=True)

    verified_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="verified_vendor_kycs",
        null=True,
        blank=True
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.business_name} KYC"


class VendorApplication(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vendor_applications")

    business_name = models.CharField(max_length=300)
    business_description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)

    support_email = models.EmailField()
    support_phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Enter a valid 10-digit mobile number.'
            )
        ]
    )

    business_address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        db_index=True
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviewed_vendor_applications",
        null=True,
        blank=True
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} ({self.status})"


class VendorBankAccount(models.Model):
    ifsc_validator = RegexValidator(
        regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
        message='Enter a valid IFSC code.'
    )
    vendor = models.ForeignKey(
        VendorProfile,
        on_delete=models.PROTECT,
        related_name="bank_accounts"
    )
    account_holder_name = models.CharField(max_length=80)
    bank_name = models.CharField(max_length=80)
    account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(
        max_length=11,
        validators=[ifsc_validator]
    )
    is_primary = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            VendorBankAccount.objects.filter(
                vendor=self.vendor,
                is_primary=True
            ).exclude(
                pk=self.pk
            ).update(is_primary=False)

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor"],
                condition=models.Q(is_primary=True),
                name="unique_primary_bank_account_per_vendor",
            )
        ]

    def __str__(self):
        return f"{self.bank_name} - {self.account_holder_name}"
