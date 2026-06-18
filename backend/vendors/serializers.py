from rest_framework import serializers
from vendors.models import VendorApplication, VendorProfile, VendorKYC, VendorBankAccount


class VendorApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = [
            "business_name",
            "business_description",
            "logo",
            "support_email",
            "support_phone",
            "business_address"
        ]

    def validate(self, attrs):
        user = self.context["request"].user

        if VendorProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("Yor are already a vendor.")

        if VendorApplication.objects.filter(user=user, status="Pending").exists():
            raise serializers.ValidationError(
                "You already have a pending application.")

        return attrs

    def create(self, validated_data):
        vendor = VendorApplication.objects.create(
            user=self.context["request"].user,
            **validated_data
        )
        return vendor


class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = "__all__"


class VendorApplicationReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["Approved", "Rejected"]
    )
    remarks = serializers.CharField(
        required=False,
        allow_blank=True
    )


class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = (
            "id",
            "business_name",
            "business_description",
            "logo",
            "support_email",
            "support_phone",
            "business_address",
            "commission_percentage",
            "rating",
            "kyc_verified",
            "is_active",
            "created_at",
            "updated_at"
        )

        read_only_fields = (
            "id",
            "business_name",
            "commission_percentage",
            "rating",
            "kyc_verified",
            "is_active",
            "created_at",
            "updated_at"
        )


class VendorDashboardSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField()
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, allow_null=True)
    kyc_documents_uploaded = serializers.BooleanField()
    is_active = serializers.BooleanField()


class VendorKYCCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorKYC
        fields = (
            "gst_number",
            "pan_number",
            "gst_document",
            "pan_document",
        )

    def validate(self, attrs):
        vendor = self.context["request"].user.vendor_profile

        kyc = VendorKYC.objects.filter(
            vendor=vendor
        ).first()

        if kyc:
            if kyc.verification_status == "PENDING":
                raise serializers.ValidationError(
                    "Your KYC is under review."
                )

            if kyc.verification_status == "APPROVED":
                raise serializers.ValidationError(
                    "Your KYC is already approved."
                )

        return attrs


class VendorKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorKYC
        fields = "__all__"


class VendorKYCReviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["APPROVED", "REJECTED"]
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True
    )


class VendorBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBankAccount
        fields = (
            "id",
            "account_holder_name",
            "bank_name",
            "account_number",
            "ifsc_code",
            "is_primary",
            "created_at",
            "updated_at"
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at"
        )
