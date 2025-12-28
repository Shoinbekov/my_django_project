from rest_framework import serializers
from typing import Dict, Any

from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for displaying basic user information."""
    
    class Meta:
        model = User
        fields = ("id", "email", "username")


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password hashing."""
    
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create and return a new user with encrypted password."""
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
