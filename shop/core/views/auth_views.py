from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from django.contrib.auth import authenticate

from core.serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """User login endpoint."""
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Handle user login and return JWT tokens."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email: str = serializer.validated_data["email"]
        password: str = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })