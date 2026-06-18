from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from rest_framework import generics, viewsets
from rest_framework import status

from accounts.permissions import IsAdminGroup, IsVendorGroup

from .models import VendorProfile, VendorApplication, VendorKYC, VendorPreviousKYC, VendorBankAccount
from .serializers import VendorApplicationCreateSerializer, VendorApplicationSerializer, VendorApplicationReviewSerializer, VendorProfileSerializer, VendorDashboardSerializer, VendorKYCCreateSerializer, VendorKYCSerializer, VendorKYCReviewSerializer, VendorBankAccountSerializer
from .utils import approve_application, reject_application, send_vendor_email


# Create your views here.
class VendorApplicationEligibilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if VendorProfile.objects.filter(user=request.user).exists():
            return Response(
                {
                    "can_apply": False,
                    "reason": "You are already a vendor."
                },
                status=status.HTTP_200_OK
            )

        if VendorApplication.objects.filter(user=request.user, status="PENDING").exists():
            return Response(
                {
                    "can_apply": False,
                    "reason": "You already have a pending application."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "can_apply": True
            },
            status=status.HTTP_200_OK
        )


class ApplyVendorApplicationView(generics.CreateAPIView):
    serializer_class = VendorApplicationCreateSerializer
    permission_classes = [IsAuthenticated]


class MyApplicationsView(generics.ListAPIView):
    serializer_class = VendorApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            VendorApplication.objects
            .filter(user=self.request.user)
            .order_by("-created_at")
        )


class AdminVendorApplicationsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorApplicationSerializer
    permission_classes = [IsAdminGroup]

    queryset = (
        VendorApplication.objects
        .select_related("user", "reviewed_by")
        .order_by("-created_at")
    )

    @action(detail=True, methods=["patch"], url_path="review")
    def review(self, request, pk=None):
        application = self.get_object()
        serializer = VendorApplicationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status_value = serializer.validated_data['status']
        remarks = serializer.validated_data.get("remarks", "")

        if status_value == "APPROVED":
            approve_application(application=application,
                                admin_user=request.user)
            message = """
                Your vendor application has been approved by our team.

                Current Status: APPROVED
            """
        else:
            reject_application(application=application,
                               admin_user=request.user, remarks=remarks)

            message = """
                Your vendor application has been rejected by our team.

                Current Status: REJECTED
            """
            if remarks:
                message += f"\n\nReason: {remarks}"

        subject = "Vendor Application Status Updated"
        send_vendor_email(application, subject, message)
        return Response(
            {
                "message": f"Application {status_value.lower()} successfully."
            },
            status=status.HTTP_200_OK
        )


class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsVendorGroup]

    def get_object(self):
        return self.request.user.vendor_profile


class VendorDashboardView(APIView):
    permission_classes = [IsVendorGroup]

    def get(self, request):
        vendor = request.user.vendor_profile
        serializer = VendorDashboardSerializer({
            "business_name": vendor.business_name,
            "rating": vendor.rating,
            "kyc_documents_uploaded": vendor.kyc_documents_uploaded,
            "kyc_verified": vendor.kyc_verified,
            "is_active": vendor.is_active,
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorKYCCreateView(generics.CreateAPIView):
    serializer_class = VendorKYCCreateSerializer
    permission_classes = [IsVendorGroup]

    def perform_create(self, serializer):
        vendor = self.request.user.vendor_profile

        existing_kyc = VendorKYC.objects.filter(vendor=vendor).first()

        if existing_kyc:
            VendorPreviousKYC.objects.create(
                vendor=existing_kyc.vendor,
                gst_number=existing_kyc.gst_number,
                pan_number=existing_kyc.pan_number,
                gst_document=existing_kyc.gst_document,
                pan_document=existing_kyc.pan_document,
                verification_status=existing_kyc.verification_status,
                remarks=existing_kyc.remarks,
                verified_by=existing_kyc.verified_by,
                verified_at=existing_kyc.verified_at
            )
            existing_kyc.gst_number = serializer.validated_data["gst_number"]
            existing_kyc.pan_number = serializer.validated_data["pan_number"]
            existing_kyc.gst_document = serializer.validated_data["gst_document"]
            existing_kyc.pan_document = serializer.validated_data["pan_document"]
            existing_kyc.remarks = None
            existing_kyc.verified_by = None
            existing_kyc.verified_at = None
            existing_kyc.verification_status = "PENDING"
            vendor.kyc_verified = False

            existing_kyc.save()
        else:
            serializer.save(vendor=vendor)

        vendor.kyc_documents_uploaded = True
        vendor.save(
            update_fields=[
                "kyc_documents_uploaded",
                "kyc_verified"
            ]
        )


class AdminVendorKYCViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorKYCSerializer
    permission_classes = [IsAdminGroup]

    queryset = (
        VendorKYC.objects
        .select_related("vendor", "verified_by")
        .order_by("-created_at")
    )

    @action(detail=True, methods=["patch"], url_path="review")
    def review(self, request, pk=None):
        kyc = self.get_object()

        serializer = VendorKYCReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status_value = serializer.validated_data["status"]

        remarks = serializer.validated_data.get("remarks", "")

        vendor = kyc.vendor

        if status_value == "APPROVED":
            kyc.verification_status = "APPROVED"
            kyc.remarks = None
            vendor.kyc_verified = True
            message = """
                Your KYC review status has been updated by our team.

                Current Status: APPROVED
            """
        elif status_value == "REJECTED":
            kyc.verification_status = "REJECTED"
            kyc.remarks = remarks
            vendor.kyc_verified = False
            message = """
                Your KYC review status has been updated by our team.

                Current Status: REJECTED
            """
            if remarks:
                message += f"\n\nReason: {remarks}"

        kyc.verified_by = request.user
        kyc.verified_at = timezone.now()
        kyc.save()

        vendor.save(
            update_fields=[
                "kyc_verified"
            ]
        )

        subject = "KYC Status Updated"
        send_vendor_email(kyc, subject, message)

        return Response(
            {
                "message": f"KYC {status_value.lower()} successfully."
            },
            status=status.HTTP_200_OK
        )


class VendorBankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = VendorBankAccountSerializer
    permission_classes = [IsVendorGroup]

    def get_queryset(self):
        return (
            VendorBankAccount.objects
            .filter(vendor=self.request.user.vendor_profile)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor_profile)


class AdminVendorBankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorBankAccountSerializer
    permission_classes = [IsAdminGroup]

    queryset = (
        VendorBankAccount.objects
        .select_related("vendor")
        .order_by("-created_at")
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get("vendor_id")

        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)

        return queryset
