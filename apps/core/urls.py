from django.urls import path

from apps.core.views import (
    RegisterView,
    LoginView,
    CategoryListView,
    ProductListView,
    ProductDetailView,
    CartView,
    CartAddItemView,
    CartRemoveItemView,
    CartUpdateItemView,
    OrderListCreateView,
    PaymentListView
)

urlpatterns = [
    # AUTH
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    
    # CATEGORIES
    path("categories/", CategoryListView.as_view(), name="category-list"),
    
    # PRODUCTS
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    
    # CART
    path("cart/current/", CartView.as_view(), name="cart-detail"),
    path("cart/add_item/", CartAddItemView.as_view(), name="cart-add"),
    path("cart/remove_item/", CartRemoveItemView.as_view(), name="cart-remove"),
    path("cart/update_item/", CartUpdateItemView.as_view(), name="cart-update"),
    
    # ORDERS
    path("orders/", OrderListCreateView.as_view(), name="orders"),
    
    # PAYMENTS
    path("payments/", PaymentListView.as_view(), name="payments"),
]
