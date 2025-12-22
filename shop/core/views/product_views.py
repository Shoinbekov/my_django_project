from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Category, Product
from core.serializers import CategorySerializer, ProductSerializer
from core.permissions import IsAdminOrReadOnly


class CategoryListView(generics.ListAPIView):
    """List all product categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListCreateAPIView):
    """
    List all products or create a new product.

    Features:
    - Filter by category: ?category=1
    - Search by title or description: ?search=iphone
    - Ordering: ?ordering=price or ?ordering=-price
    """
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Enable filtering, search, and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Filtering fields
    filterset_fields = ["category"]

    # Search fields
    search_fields = ["title", "description"]

    # Ordering fields
    ordering_fields = ["price", "title", "stock"]
    ordering = ["-id"]  # Default: newest first


class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve details of a specific product by its ID."""
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
