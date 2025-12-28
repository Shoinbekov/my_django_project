from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.models import Order, Payment
from apps.core.serializers import OrderSerializer, PaymentSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List the current user's orders or create a new one.

    Supports:
    - Ordering by creation date or total price: ?ordering=-created_at or ?ordering=total_price
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    # Enable ordering
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]  # Default ordering: newest first

    def get_queryset(self):
        """Return orders belonging to the current user, including related products."""
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")

    def perform_create(self, serializer) -> None:
        """Save a new order for the current user."""
        serializer.save(user=self.request.user)


class PaymentListView(generics.ListAPIView):
    """
    List all payments.

    Supports:
    - Filtering by status and method: ?status=completed, ?method=card
    - Ordering by amount or ID: ?ordering=-created_at
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Enable filtering and ordering
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Filtering
    filterset_fields = ["status", "method"]

    # Ordering
    ordering_fields = ["amount", "created_at"]
    ordering = ["-id"]  # Default ordering: newest first
