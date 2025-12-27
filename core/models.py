from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class User(AbstractUser):
    """Custom user model using email as username."""
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email


class Category(models.Model):
    """Product category model."""
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Product model with category relationship."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    """Shopping cart for authenticated users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Cart of {self.user.email}"

    def get_total_price(self) -> Decimal:
        """Calculate total price of all items in cart."""
        total = sum(
            item.product.price * item.quantity 
            for item in self.items.all()
        )
        return Decimal(str(total))


class CartItem(models.Model):
    """Individual item in shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item."""
        return self.product.price * self.quantity


class Order(models.Model):
    """Customer order model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """Individual item in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"


class Payment(models.Model):
    """Payment information for orders."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Payment for Order #{self.order.id}"