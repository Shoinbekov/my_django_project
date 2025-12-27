from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from core.models import Cart, Product
from core.serializers import CartSerializer
from core.services import add_item_to_cart, remove_item_from_cart, update_item_quantity


class CartView(generics.RetrieveAPIView):
    """Retrieve the current user's shopping cart or create one if it doesn't exist."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self) -> Cart:
        return Cart.objects.get_or_create(user=self.request.user)[0]


class CartAddItemView(APIView):
    """Endpoint to add a product to the shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        add_item_to_cart(request.user, product, quantity)
        return Response({"message": "Item added successfully"}, status=status.HTTP_200_OK)


class CartRemoveItemView(APIView):
    """Endpoint to remove a product from the shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request) -> Response:
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        removed = remove_item_from_cart(request.user, product_id)
        if not removed:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Item removed successfully"}, status=status.HTTP_200_OK)


class CartUpdateItemView(APIView):
    """Endpoint to update the quantity of a product in the shopping cart."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request) -> Response:
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or quantity is None:
            return Response(
                {"error": "product_id and quantity are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated = update_item_quantity(request.user, product_id, int(quantity))
        if not updated:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Quantity updated successfully"}, status=status.HTTP_200_OK)
