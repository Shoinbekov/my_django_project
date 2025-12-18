from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Category, Product
from core.serializers import CategorySerializer, ProductSerializer
from core.permissions import IsAdminOrReadOnly


class CategoryListView(generics.ListAPIView):
    """List all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    
    Supports:
    - Filtering by category: ?category=1
    - Search: ?search=iphone
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
    
    # Filtering
    filterset_fields = ["category"]
    
    # Search by title and description
    search_fields = ["title", "description"]
    
    # Ordering by price and title
    ordering_fields = ["price", "title", "stock"]
    ordering = ["-id"]  # Default ordering


class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a specific product by ID."""
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer