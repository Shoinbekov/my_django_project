from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import User, Category, Product, Cart, Order


# ============================================================
# AUTH TESTS (REGISTER + LOGIN)
# ============================================================

class AuthTests(APITestCase):

    def test_register_success(self):
        """GOOD — успешная регистрация"""
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "123456"
        }
        r = self.client.post("/api/register/", data)
        self.assertEqual(r.status_code, 201)

    def test_register_missing_email(self):
        """BAD — нет email"""
        r = self.client.post("/api/register/", {"username": "a", "password": "123"})
        self.assertEqual(r.status_code, 400)

    def test_register_missing_password(self):
        """BAD — нет password"""
        r = self.client.post("/api/register/", {"email": "a@a.com", "username": "a"})
        self.assertEqual(r.status_code, 400)

    def test_register_invalid_email(self):
        """BAD — неверный email"""
        r = self.client.post("/api/register/", {"email": "wrong", "username": "a", "password": "123"})
        self.assertEqual(r.status_code, 400)

    def test_login_success(self):
        """GOOD — логин проходит"""
        User.objects.create_user(email="user@mail.com", username="u", password="123456")
        r = self.client.post("/api/login/", {"email": "user@mail.com", "password": "123456"})
        self.assertEqual(r.status_code, 200)

    def test_login_wrong_password(self):
        """BAD — неправильный пароль"""
        User.objects.create_user(email="tmp@mail.com", username="u2", password="correct")
        r = self.client.post("/api/login/", {"email": "tmp@mail.com", "password": "wrong"})
        self.assertEqual(r.status_code, 400)

    def test_login_missing_email(self):
        """BAD — нет email"""
        r = self.client.post("/api/login/", {"password": "123"})
        self.assertEqual(r.status_code, 400)

    def test_login_missing_password(self):
        """BAD — нет password"""
        r = self.client.post("/api/login/", {"email": "user@mail.com"})
        self.assertEqual(r.status_code, 400)



# ============================================================
# PRODUCT TESTS
# ============================================================

class ProductTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Phones")
        Product.objects.create(
            title="iPhone",
            description="test",
            price=1000,
            stock=5,
            category=self.category
        )

    def test_products_success(self):
        """GOOD — /api/products/ работает"""
        r = self.client.get("/api/products/")
        self.assertEqual(r.status_code, 200)

    def test_products_wrong_url(self):
        """BAD — неправильный URL"""
        r = self.client.get("/api/wrong/")
        self.assertEqual(r.status_code, 404)

    def test_products_wrong_method(self):
        """BAD — POST запрещён"""
        r = self.client.post("/api/products/", {})
        self.assertIn(r.status_code, [401, 403, 405])

    def test_product_not_found(self):
        """BAD — товара нет"""
        r = self.client.get("/api/products/999/")
        self.assertEqual(r.status_code, 404)



# ============================================================
# CATEGORY TESTS
# ============================================================

class CategoryTests(APITestCase):

    def setUp(self):
        Category.objects.create(name="Sports")

    def test_category_success(self):
        """GOOD — категории работают"""
        r = self.client.get("/api/categories/")
        self.assertEqual(r.status_code, 200)

    def test_category_wrong_url(self):
        """BAD — неправильный URL"""
        r = self.client.get("/api/categoryzz/")
        self.assertEqual(r.status_code, 404)

    def test_category_post_not_allowed(self):
        """BAD — POST запрещён"""
        r = self.client.post("/api/categories/", {})
        self.assertIn(r.status_code, [401, 403, 405])

    def test_category_detail_not_found(self):
        """BAD — категории нет"""
        r = self.client.get("/api/categories/999/")
        self.assertEqual(r.status_code, 404)



# ============================================================
# CART TESTS
# ============================================================

class CartTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="cart@mail.com", username="cart", password="123456"
        )
        self.cart = Cart.objects.create(user=self.user)  # <-- ВАЖНО! ДОБАВЛЕНО!
        self.client = APIClient()

    def authenticate(self):
        r = self.client.post("/api/login/", {
            "email": "cart@mail.com",
            "password": "123456"
        })
        token = r.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_cart_requires_auth(self):
        """BAD — без токена корзина недоступна"""
        r = self.client.get("/api/cart/")
        self.assertEqual(r.status_code, 401)

    def test_cart_success(self):
        """GOOD — корзина возвращается"""
        self.authenticate()
        r = self.client.get("/api/cart/")
        self.assertEqual(r.status_code, 200)

    def test_cart_wrong_url(self):
        """BAD — неправильный URL"""
        self.authenticate()
        r = self.client.get("/api/cartszzz/")
        self.assertEqual(r.status_code, 404)

    def test_cart_method_not_allowed(self):
        """BAD — POST не разрешён"""
        self.authenticate()
        r = self.client.post("/api/cart/", {})
        self.assertIn(r.status_code, [403, 405])



# ============================================================
# ORDER TESTS
# ============================================================

class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="order@mail.com", username="order", password="123456"
        )
        self.client = APIClient()
        self.authenticate()

    def authenticate(self):
        r = self.client.post("/api/login/", {
            "email": "order@mail.com",
            "password": "123456"
        })
        token = r.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_order_success(self):
        """GOOD — доступ разрешён"""
        r = self.client.get("/api/orders/")
        self.assertEqual(r.status_code, 200)

    def test_order_auth_required(self):
        """BAD — без токена нельзя"""
        client = APIClient()  # без токена
        r = client.get("/api/orders/")
        self.assertEqual(r.status_code, 401)

    def test_order_wrong_url(self):
        """BAD — неправильный URL"""
        r = self.client.get("/api/orderrrr/")
        self.assertEqual(r.status_code, 404)

    def test_order_method_not_allowed(self):
        """BAD — DELETE запрещён"""
        r = self.client.delete("/api/orders/")
        self.assertIn(r.status_code, [403, 405])
