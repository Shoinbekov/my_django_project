from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from apps.core.serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    """Endpoint for user registration."""
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """Endpoint for user login and JWT token retrieval."""
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Authenticate user and return access and refresh tokens."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
