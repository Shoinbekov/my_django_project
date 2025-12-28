from rest_framework import serializers

from apps.core.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products, including all fields."""
    
    class Meta:
        model = Product
        fields = "__all__"
