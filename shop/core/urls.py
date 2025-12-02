from django.urls import path
from .views import (
    CartView,
    CartAddItemView,
    CartRemoveItemView,
    CartUpdateItemView,
    OrderListCreateView
)

urlpatterns = [
    # CART
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("cart/add/", CartAddItemView.as_view(), name="cart-add"),
    path("cart/remove/<int:product_id>/", CartRemoveItemView.as_view(), name="cart-remove"),
    path("cart/update/<int:product_id>/", CartUpdateItemView.as_view(), name="cart-update"),

    # ORDERS
    path("orders/", OrderListCreateView.as_view(), name="orders"),
]
