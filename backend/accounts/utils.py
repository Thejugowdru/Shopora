from rest_framework_simplejwt.tokens import RefreshToken
import uuid


def get_auth_response(user):
    refresh = RefreshToken.for_user(user)

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "is_active": user.is_active,
            "role": user.role,
            "group_id": user.group.id,
            "created_at": user.created_at
        },
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
