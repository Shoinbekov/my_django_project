from rest_framework import serializers

from core.models import Order, OrderItem, Payment
from .product_serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments."""
    class Meta:
        model = Payment
        fields = "__all__"