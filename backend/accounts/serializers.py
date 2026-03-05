from rest_framework import serializers
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username',  'date_of_birth',
                  'gender', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Password doesn\'t match'
            })
        return super().validate(data)

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)

        customer_group = Group.objects.get(name='Customer')
        user.groups.set([customer_group])

        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')
        try:
            user = User.objects.get(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier)
            )
        except User.DoesNotExist:
            # # 👇 Default key non_field_errors, In react error.response.data.non_field_errors
            # raise serializers.ValidationError('Invalid credentials')

            # # 👇 In react error.response.data.detail
            raise serializers.ValidationError({
                'detail': 'Invalid credentials'
            })

        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError({
                'detail': 'Invalid credentials'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'Your account is disabled'
            })

        return user
