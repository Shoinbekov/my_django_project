from typing import Tuple
from decimal import Decimal

from core.models import Cart, CartItem, Product, User


def get_or_create_cart(user: User) -> Cart:
    """Get or create cart for user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def add_item_to_cart(user: User, product: Product, quantity: int) -> Tuple[CartItem, bool]:
    """
    Add item to cart or update quantity.
    
    Returns:
        Tuple of (CartItem, created: bool)
    """
    cart = get_or_create_cart(user)
    
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity}
    )
    
    if not created:
        item.quantity += quantity
        item.save()
    
    return item, created


def remove_item_from_cart(user: User, product_id: int) -> bool:
    """
    Remove item from cart.
    
    Returns:
        True if item was removed, False if not found.
    """
    try:
        cart = Cart.objects.get(user=user)
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.delete()
        return True
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return False


def update_item_quantity(user: User, product_id: int, quantity: int) -> bool:
    """
    Update item quantity in cart.
    
    Returns:
        True if updated, False if not found.
    """
    try:
        cart = Cart.objects.get(user=user)
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.quantity = quantity
        item.save()
        return True
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return False


def calculate_cart_total(cart: Cart) -> Decimal:
    """Calculate total price of cart."""
    total = sum(
        item.product.price * item.quantity 
        for item in cart.items.all()
    )
    return Decimal(str(total))