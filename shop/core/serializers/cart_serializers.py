from rest_framework import serializers

from core.models import Cart, CartItem
from .product_serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for individual items in the shopping cart."""
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the shopping cart, including all items."""
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
