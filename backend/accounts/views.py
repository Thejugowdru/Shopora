from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random
import time

from django.core.cache import cache
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

from .models import User, Address
from .permissions import IsAdminGroup
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, UserSerializer, AddressSerializer, SendOTPSerializer


# Create your views here.
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    OTP_EXPIRY = 300      # 5 minutes
    COOLDOWN_TIME = 60    # 1 minute

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        if User.objects.filter(
            email=email
        ).exists():
            raise ValidationError({
                "email": "Email already registered."
            })

        cooldown_key = (
            f"shopora:auth:cooldown:{email}"
        )

        if cache.get(cooldown_key):
            raise ValidationError({
                "email":
                "Please wait 1 minute before requesting another OTP."
            })

        otp = str(
            random.randint(
                100000,
                999999
            )
        )

        otp_key = (
            f"shopora:auth:otp:{email}"
        )

        cache.set(
            otp_key,
            otp,
            timeout=self.OTP_EXPIRY
        )

        cache.set(
            cooldown_key,
            True,
            timeout=self.COOLDOWN_TIME
        )

        start = time.perf_counter()
        send_mail(
            subject="Shopora Email Verification",
            message=(
                f"Your Shopora OTP is {otp}. "
                f"It is valid for 5 minutes."
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False
        )
        print(f"Email time: {time.perf_counter() - start:.2f}s")

        return Response(
            {
                "message": "OTP sent successfully."
            },
            status=status.HTTP_200_OK
        )


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not old_password:
            raise ValidationError({
                "old_password": "This field is required."
            })

        if not new_password:
            raise ValidationError({
                "new_password": "This field is required."
            })

        if not confirm_password:
            raise ValidationError({
                "confirm_password": "This field is required."
            })

        if not request.user.check_password(old_password):
            raise ValidationError({
                "old_password": "Incorrect password."
            })

        if new_password != confirm_password:
            raise ValidationError({
                "confirm_password": "Passwords do not match."
            })
        request.user.set_password(new_password)
        request.user.temp_password = False
        request.user.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK
        )


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminGroup]
    queryset = User.objects.select_related("group")
    serializer_class = UserSerializer

    @action(detail=True, methods=["post"])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password:
            raise ValidationError({
                "new_password": "This field is required."
            })

        if not confirm_password:
            raise ValidationError({
                "confirm_password": "This field is required."
            })

        if new_password != confirm_password:
            raise ValidationError({
                "confirm_password": "Passwords do not match."
            })

        user.set_password(new_password)
        user.temp_password = False
        user.save()

        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )


class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            RefreshToken(
                request.data["refresh"]
            ).blacklist()

            return Response(
                {
                    "message": "Logged out successfully."
                },
                status=status.HTTP_200_OK
            )

        except KeyError:
            raise ValidationError({
                "refresh": "This field is required."
            })

        except Exception:
            raise ValidationError({
                "refresh": "Invalid or expired token."
            })
