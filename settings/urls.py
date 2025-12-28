from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from apps.core.views import (
    RegisterView, LoginView,
    ProductListView, ProductDetailView,
    CategoryListView, OrderListCreateView, PaymentListView
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Auth
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),

    # Products
    path("api/products/", ProductListView.as_view(), name="product-list"),
    path("api/products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),

    # Categories
    path("api/categories/", CategoryListView.as_view(), name="category-list"),

    # Orders (duplicate for Swagger)
    path("api/orders/", OrderListCreateView.as_view(), name="orders"),

    # Payments
    path("api/payments/", PaymentListView.as_view(), name="payments"),

    # --- API Documentation (Swagger) ---
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Core application — cart + advanced logic
    path("api/", include("apps.core.urls")),
]
