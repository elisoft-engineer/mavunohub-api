from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class EmailPasswordTokenObtainSerializer(TokenObtainPairSerializer):
    """
    Serializer for Email-Password authentication
    """

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        return self.generate_auth_response(user)
    
    @classmethod
    def generate_auth_response(cls, user):
        refresh = RefreshToken.for_user(user)
        user_data = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "phone": getattr(user.phone, "as_e164", None),
            "location": user.location,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "created_at": str(user.created_at),
            "updated_at": str(user.updated_at),
        }

        return {
            "user": user_data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
