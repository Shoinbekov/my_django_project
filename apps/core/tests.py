import pytest
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from apps.core.models import User, Category, Product, Cart, CartItem, Order, Payment


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def api_client():
    """API client fixture."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='adminpass123'
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(name='Electronics')


@pytest.fixture
def product(db, category):
    """Create a test product."""
    return Product.objects.create(
        category=category,
        title='iPhone',
        description='Test product',
        price=Decimal('1000.00'),
        stock=10
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Client authenticated with regular user."""
    response = api_client.post('/api/auth/login/', {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Client authenticated with admin user."""
    response = api_client.post('/api/auth/login/', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


# ============================================================
# AUTH TESTS (REGISTER)
# ============================================================

@pytest.mark.django_db
class TestAuthRegister:
    """Tests for user registration endpoint."""
    
    def test_register_success(self, api_client) -> None:
        """GOOD — successful registration"""
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "securepass123"
        }
        response = api_client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_register_missing_email(self, api_client) -> None:
        """BAD — missing email"""
        response = api_client.post("/api/auth/register/", {
            "username": "user",
            "password": "123456"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_missing_password(self, api_client) -> None:
        """BAD — missing password"""
        response = api_client.post("/api/auth/register/", {
            "email": "user@example.com",
            "username": "user"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_email(self, api_client) -> None:
        """BAD — invalid email format"""
        response = api_client.post("/api/auth/register/", {
            "email": "not-an-email",
            "username": "user",
            "password": "123456"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ============================================================
# AUTH TESTS (LOGIN)
# ============================================================

@pytest.mark.django_db
class TestAuthLogin:
    """Tests for user login endpoint."""
    
    def test_login_success(self, api_client, user) -> None:
        """GOOD — successful login"""
        response = api_client.post("/api/auth/login/", {
            "email": "test@example.com",
            "password": "testpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_wrong_password(self, api_client, user) -> None:
        """BAD — wrong password"""
        response = api_client.post("/api/auth/login/", {
            "email": "test@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_missing_email(self, api_client) -> None:
        """BAD — missing email"""
        response = api_client.post("/api/auth/login/", {
            "password": "123456"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_missing_password(self, api_client, user) -> None:
        """BAD — missing password"""
        response = api_client.post("/api/auth/login/", {
            "email": "test@example.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ============================================================
# CATEGORY TESTS
# ============================================================

@pytest.mark.django_db
class TestCategories:
    """Tests for category endpoints."""
    
    def test_category_list_success(self, api_client, category) -> None:
        """GOOD — list categories works"""
        response = api_client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_category_wrong_url(self, api_client) -> None:
        """BAD — wrong URL"""
        response = api_client.get("/api/categoriesxxx/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_category_post_not_allowed(self, api_client) -> None:
        """BAD — POST not allowed"""
        response = api_client.post("/api/categories/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_category_detail_not_found(self, api_client) -> None:
        """BAD — category not found"""
        response = api_client.get("/api/categories/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# PRODUCT TESTS
# ============================================================

@pytest.mark.django_db
class TestProducts:
    """Tests for product endpoints."""
    
    def test_products_list_success(self, api_client, product) -> None:
        """GOOD — list products works"""
        response = api_client.get("/api/products/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_products_wrong_url(self, api_client) -> None:
        """BAD — wrong URL"""
        response = api_client.get("/api/productsxxx/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_products_create_unauthorized(self, api_client, category) -> None:
        """BAD — cannot create without authentication"""
        response = api_client.post("/api/products/", {
            "category": category.id,
            "title": "New Product",
            "description": "Test",
            "price": "999.99",
            "stock": 5
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_product_detail_not_found(self, api_client) -> None:
        """BAD — product not found"""
        response = api_client.get("/api/products/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# CART TESTS (GET)
# ============================================================

@pytest.mark.django_db
class TestCartGet:
    """Tests for cart retrieval endpoint."""
    
    def test_cart_get_success(self, authenticated_client) -> None:
        """GOOD — get cart works"""
        response = authenticated_client.get("/api/cart/current/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_cart_unauthorized(self, api_client) -> None:
        """BAD — requires authentication"""
        response = api_client.get("/api/cart/current/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cart_wrong_url(self, authenticated_client) -> None:
        """BAD — wrong URL"""
        response = authenticated_client.get("/api/cart/wrong/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_cart_wrong_method(self, authenticated_client) -> None:
        """BAD — wrong HTTP method"""
        response = authenticated_client.post("/api/cart/current/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ============================================================
# CART TESTS (ADD ITEM)
# ============================================================

@pytest.mark.django_db
class TestCartAddItem:
    """Tests for adding items to cart."""
    
    def test_cart_add_item_success(self, authenticated_client, product) -> None:
        """GOOD — add item to cart"""
        response = authenticated_client.post("/api/cart/add_item/", {
            "product_id": product.id,
            "quantity": 2
        })
        assert response.status_code == status.HTTP_200_OK
    
    def test_cart_add_item_unauthorized(self, api_client, product) -> None:
        """BAD — requires authentication"""
        response = api_client.post("/api/cart/add_item/", {
            "product_id": product.id,
            "quantity": 1
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cart_add_item_missing_product_id(self, authenticated_client) -> None:
        """BAD — missing product_id"""
        response = authenticated_client.post("/api/cart/add_item/", {
            "quantity": 1
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_cart_add_item_product_not_found(self, authenticated_client) -> None:
        """BAD — product not found"""
        response = authenticated_client.post("/api/cart/add_item/", {
            "product_id": 99999,
            "quantity": 1
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# CART TESTS (REMOVE ITEM) - FIXED: product_id in body
# ============================================================

@pytest.mark.django_db
class TestCartRemoveItem:
    """Tests for removing items from cart."""
    
    def test_cart_remove_item_success(self, authenticated_client, product, user) -> None:
        """GOOD — remove item from cart"""
        # First add item
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        
        # Send product_id in request body
        response = authenticated_client.delete("/api/cart/remove_item/", {
            "product_id": product.id
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_cart_remove_item_unauthorized(self, api_client, product) -> None:
        """BAD — requires authentication"""
        response = api_client.delete("/api/cart/remove_item/", {
            "product_id": product.id
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cart_remove_item_missing_product_id(self, authenticated_client) -> None:
        """BAD — missing product_id"""
        response = authenticated_client.delete("/api/cart/remove_item/", {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_cart_remove_item_not_found(self, authenticated_client) -> None:
        """BAD — item not in cart"""
        response = authenticated_client.delete("/api/cart/remove_item/", {
            "product_id": 99999
        }, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# CART TESTS (UPDATE ITEM) - FIXED: product_id in body
# ============================================================

@pytest.mark.django_db
class TestCartUpdateItem:
    """Tests for updating cart item quantity."""
    
    def test_cart_update_item_success(self, authenticated_client, product, user) -> None:
        """GOOD — update item quantity"""
        # First add item
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        
        # Send product_id and quantity in request body
        response = authenticated_client.patch("/api/cart/update_item/", {
            "product_id": product.id,
            "quantity": 5
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
    
    def test_cart_update_item_unauthorized(self, api_client, product) -> None:
        """BAD — requires authentication"""
        response = api_client.patch("/api/cart/update_item/", {
            "product_id": product.id,
            "quantity": 5
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_cart_update_item_missing_quantity(self, authenticated_client, product) -> None:
        """BAD — missing quantity"""
        response = authenticated_client.patch("/api/cart/update_item/", {
            "product_id": product.id
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_cart_update_item_not_found(self, authenticated_client) -> None:
        """BAD — item not in cart"""
        response = authenticated_client.patch("/api/cart/update_item/", {
            "product_id": 99999,
            "quantity": 5
        }, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================
# ORDER TESTS
# ============================================================

@pytest.mark.django_db
class TestOrders:
    """Tests for order endpoints."""
    
    def test_orders_list_success(self, authenticated_client) -> None:
        """GOOD — list orders works"""
        response = authenticated_client.get("/api/orders/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_orders_unauthorized(self, api_client) -> None:
        """BAD — requires authentication"""
        response = api_client.get("/api/orders/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_orders_wrong_url(self, authenticated_client) -> None:
        """BAD — wrong URL"""
        response = authenticated_client.get("/api/ordersxxx/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_orders_delete_not_allowed(self, authenticated_client) -> None:
        """BAD — DELETE not allowed"""
        response = authenticated_client.delete("/api/orders/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ============================================================
# PAYMENT TESTS
# ============================================================

@pytest.mark.django_db
class TestPayments:
    """Tests for payment endpoints."""
    
    def test_payments_list_success(self, api_client) -> None:
        """GOOD — list payments works"""
        response = api_client.get("/api/payments/")
        assert response.status_code == status.HTTP_200_OK
    
    def test_payments_wrong_url(self, api_client) -> None:
        """BAD — wrong URL"""
        response = api_client.get("/api/paymentsxxx/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_payments_post_not_allowed(self, api_client) -> None:
        """BAD — POST not allowed"""
        response = api_client.post("/api/payments/", {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_payment_detail_not_found(self, api_client) -> None:
        """BAD — payment not found"""
        response = api_client.get("/api/payments/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
