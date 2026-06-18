from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, ProfileView, ChangePasswordView, UserViewSet, AddressViewSet, SendOTPView, LogoutView

router = DefaultRouter()

router.register(
    "users",
    UserViewSet,
    basename="users"
)

router.register(
    "addresses",
    AddressViewSet,
    basename="addresses"
)

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view()
    ),

    path(
        "send-otp/",
        SendOTPView.as_view()
    ),

    path(
        "login/",
        LoginView.as_view()
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
    ),

    path(
        "profile/",
        ProfileView.as_view()
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view()
    ),

    path(
        "",
        include(router.urls)
    ),
]
