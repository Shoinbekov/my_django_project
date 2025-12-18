from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from core.models import Cart, Product
from core.serializers import CartSerializer
from core.services import (
    add_item_to_cart,
    remove_item_from_cart,
    update_item_quantity
)


class CartView(generics.RetrieveAPIView):
    """Get current user's shopping cart."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self) -> Cart:
        """Get or create cart for current user."""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartAddItemView(APIView):
    """Add item to shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Add product to cart or increase quantity."""
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {"error": "product_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Use service layer
        add_item_to_cart(request.user, product, int(quantity))

        return Response({"message": "Item added successfully"})


class CartRemoveItemView(APIView):
    """Remove item from shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request) -> Response:
        """Remove product from cart."""
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use service layer
        success = remove_item_from_cart(request.user, product_id)

        if not success:
            return Response(
                {"error": "Item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Item removed"})


class CartUpdateItemView(APIView):
    """Update item quantity in shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request) -> Response:
        """Update quantity of product in cart."""
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response(
                {"error": "product_id and quantity are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use service layer
        success = update_item_quantity(request.user, product_id, int(quantity))

        if not success:
            return Response(
                {"error": "Item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Quantity updated"})