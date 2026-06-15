from .models import User
from django.core.cache import cache
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User, Address
from .utils import get_auth_response
from django.contrib.auth import authenticate


# For Admin create the users
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


# Use Register as Customer
class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    password = serializers.CharField(write_only=True)

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "display_name",
            "email",
            "otp",
            "password",
            "confirm_password"
        ]

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password":
                "Passwords do not match."
            })

        cached_otp = cache.get(
            f"shopora:auth:otp:{attrs['email']}"
        )

        if not cached_otp:
            raise serializers.ValidationError({
                "otp": "OTP expired."
            })

        if cached_otp != attrs["otp"]:
            raise serializers.ValidationError({
                "otp": "Invalid OTP."
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop("otp")
        validated_data.pop("confirm_password")

        customer_group = Group.objects.get(
            name="CUSTOMER"
        )

        user = User.objects.create_user(
            **validated_data,
            group=customer_group,
            email_verified=True
        )

        cache.delete(
            f"shopora:auth:otp:{user.email}"
        )

        return user

    def to_representation(self, instance):
        return get_auth_response(instance)


# For Admin CRUD operations
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "display_name",
            "group",
            "password",
            "confirm_password",
            "temp_password",
            "email_verified",
            "is_active",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "email_verified",
                            "is_active", "is_staff", "created_at", "updated_at"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if (password != confirm_password):
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data['temp_password'] = True

        user = User.objects.create_user(**validated_data)

        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials!")

        if not user.is_active:
            raise serializers.ValidationError(
                "Account is disabled."
            )
        return get_auth_response(user=user)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "display_name",
            "group",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "group",
            "created_at",
            "email"
        ]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]
