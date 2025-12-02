from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminOrReadOnly
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Payment
from .serializers import (
    RegisterSerializer, LoginSerializer,
    CategorySerializer, ProductSerializer,
    CartSerializer, OrderSerializer, PaymentSerializer
)

# ============================
#      AUTH (REGISTER/LOGIN)
# ============================

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        from django.contrib.auth import authenticate
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

# ============================
#            PRODUCTS
# ============================

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filterset_fields = ["category"]
    permission_classes = [IsAdminOrReadOnly]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer

# ============================
#           CATEGORIES
# ============================

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ============================
#             CART
# ============================

class CartView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

# ADD ITEM TO CART
class CartAddItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart, created = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += int(quantity)
            item.save()

        return Response({"message": "Item added successfully"})

# REMOVE ITEM
class CartRemoveItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found"}, status=404)

        return Response({"message": "Item removed"})

# UPDATE ITEM QUANTITY
class CartUpdateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response({"error": "product_id and quantity are required"}, status=400)

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found"}, status=404)

        item.quantity = int(quantity)
        item.save()

        return Response({"message": "Quantity updated"})

# ============================
#             ORDERS
# ============================

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ============================
#            PAYMENTS
# ============================

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
