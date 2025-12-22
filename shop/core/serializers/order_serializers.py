from rest_framework import serializers

from core.models import Order, OrderItem, Payment
from .product_serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for individual items within an order."""
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders, including all related items."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments associated with orders."""
    
    class Meta:
        model = Payment
        fields = "__all__"
