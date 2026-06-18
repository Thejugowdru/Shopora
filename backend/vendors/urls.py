from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorApplicationEligibilityView, ApplyVendorApplicationView, MyApplicationsView, AdminVendorApplicationsViewSet, VendorProfileView, VendorDashboardView, VendorKYCCreateView, AdminVendorKYCViewSet, VendorBankAccountViewSet, AdminVendorBankAccountViewSet


router = DefaultRouter()

router.register(
    r"admin/vendor-applications",
    AdminVendorApplicationsViewSet,
    basename="admin-vendor-applications"
)

router.register(
    r"admin/vendor-kycs",
    AdminVendorKYCViewSet,
    basename="admin-vendor-kycs"
)

router.register(
    r"vendor-bank-accounts",
    VendorBankAccountViewSet,
    basename="vendor-bank-accounts"
)

router.register(
    r"admin/vendor-bank-accounts",
    AdminVendorBankAccountViewSet,
    basename="admin-vendor-bank-accounts"
)


urlpatterns = [
    path(
        "application/eligibility/",
        VendorApplicationEligibilityView.as_view()
    ),

    path(
        "applications/",
        ApplyVendorApplicationView.as_view()
    ),

    path(
        "applications/my/",
        MyApplicationsView.as_view()
    ),

    path(
        "profile/",
        VendorProfileView.as_view()
    ),

    path(
        "dashboard/",
        VendorDashboardView.as_view()
    ),

    path(
        "kyc/",
        VendorKYCCreateView.as_view()
    ),

    path(
        "",
        include(router.urls)
    ),
]
