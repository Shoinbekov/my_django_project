from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Order, Payment
from core.serializers import OrderSerializer, PaymentSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List user's orders or create a new order.
    
    Supports:
    - Ordering: ?ordering=-created_at or ?ordering=total_price
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    
    # Enable ordering
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]  # Default: newest first

    def get_queryset(self):
        """Get orders for current user."""
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related("items__product")

    def perform_create(self, serializer) -> None:
        """Create order for current user."""
        serializer.save(user=self.request.user)


class PaymentListView(generics.ListAPIView):
    """
    List all payments.
    
    Supports:
    - Filtering by status: ?status=completed
    - Filtering by method: ?method=card
    - Ordering: ?ordering=-created_at
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    # Enable filtering and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    
    # Filtering
    filterset_fields = ["status", "method"]
    
    # Ordering
    ordering_fields = ["amount"]
    ordering = ["-id"]