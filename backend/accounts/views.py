from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsNotAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        group = user.groups.first()

        return Response(
            {
                'message': 'Registration successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'group': group.name
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        group = user.groups.first()

        return Response(
            {
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'group': group.name
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {"error": "Refresh Token Required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"messgae": "Logout successful"},
            status=status.HTTP_200_OK
        )
