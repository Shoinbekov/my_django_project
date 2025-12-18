from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.utils.html import format_html
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, Payment


@admin.register(User)
class UserAdmin(ModelAdmin):
    """Advanced User admin with unfold styling"""
    
    list_display = ('email', 'username', 'full_name_display', 'status_badge', 'staff_badge', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('email', 'username', 'first_name', 'last_name', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    @display(description="Full Name", ordering="first_name")
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name else "-"
    
    @display(description="Status", boolean=True)
    def status_badge(self, obj):
        return obj.is_active
    
    @display(description="Staff", boolean=True)
    def staff_badge(self, obj):
        return obj.is_staff


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Advanced Category admin with product count"""
    
    list_display = ('id', 'name', 'product_count_display')
    search_fields = ('name',)
    
    @display(description="Products Count")
    def product_count_display(self, obj):
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Advanced Product admin with stock warnings and actions"""
    
    list_display = ('id', 'title', 'price_display', 'category', 'stock_status')
    search_fields = ('title', 'description')
    list_filter = ('category',)
    list_per_page = 20
    
    fieldsets = (
        ('Product Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
    )
    
    actions = ['mark_as_out_of_stock', 'mark_as_in_stock']
    
    @display(description="Price", ordering="price")
    def price_display(self, obj):
        return format_html('<strong>${}</strong>', obj.price)
    
    @display(description="Stock Status")
    def stock_status(self, obj):
        if obj.stock == 0:
            color = "red"
            status = "OUT OF STOCK"
        elif obj.stock < 10:
            color = "orange"
            status = f"LOW ({obj.stock})"
        else:
            color = "green"
            status = f"In Stock ({obj.stock})"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)
    
    @admin.action(description="Mark as out of stock")
    def mark_as_out_of_stock(self, request, queryset):
        queryset.update(stock=0)
    
    @admin.action(description="Mark as in stock")
    def mark_as_in_stock(self, request, queryset):
        queryset.update(stock=100)


class CartItemInline(admin.TabularInline):
    """Inline for cart items"""
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'item_total')
    readonly_fields = ('item_total',)
    
    def item_total(self, obj):
        if obj.product and obj.quantity:
            return format_html('<strong>${}</strong>', obj.product.price * obj.quantity)
        return "-"
    item_total.short_description = "Total"


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    """Advanced Cart admin with items inline"""
    
    list_display = ('id', 'user', 'items_count', 'cart_total_display')
    search_fields = ('user__email', 'user__username')
    inlines = [CartItemInline]
    
    @display(description="Items")
    def items_count(self, obj):
        count = obj.items.count()
        return format_html('<strong>{}</strong> items', count)
    
    @display(description="Cart Total", ordering="user")
    def cart_total_display(self, obj):
        total = sum(item.product.price * item.quantity for item in obj.items.all())
        return format_html('<strong style="color: green;">${}</strong>', total)


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    """Advanced CartItem admin"""
    
    list_display = ('cart', 'product', 'quantity', 'item_total_display')
    search_fields = ('product__title', 'cart__user__email')
    list_filter = ('cart__user',)
    
    @display(description="Item Total", ordering="quantity")
    def item_total_display(self, obj):
        total = obj.product.price * obj.quantity
        return format_html('<strong>${}</strong>', total)


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'item_total')
    readonly_fields = ('item_total',)
    
    def item_total(self, obj):
        return format_html('<strong>${}</strong>', obj.price * obj.quantity)
    item_total.short_description = "Total"


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """Advanced Order admin with items inline"""
    
    list_display = ('id', 'user', 'status_display', 'total_price_display', 'items_count', 'created_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('created_at', 'user')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'total_price')
    inlines = [OrderItemInline]
    
    actions = ['mark_as_delivered', 'mark_as_cancelled']
    
    @display(description="Status")
    def status_display(self, obj):
        return format_html('<span style="color: green; font-weight: bold;">COMPLETED</span>')
    
    @display(description="Total", ordering="total_price")
    def total_price_display(self, obj):
        return format_html('<strong style="color: green; font-size: 14px;">${}</strong>', obj.total_price)
    
    @display(description="Items")
    def items_count(self, obj):
        count = obj.items.count()
        return format_html('<strong>{}</strong> items', count)
    
    @admin.action(description="Mark as delivered")
    def mark_as_delivered(self, request, queryset):
        self.message_user(request, f"{queryset.count()} orders marked as delivered")
    
    @admin.action(description="Mark as cancelled")
    def mark_as_cancelled(self, request, queryset):
        self.message_user(request, f"{queryset.count()} orders marked as cancelled")


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    """Advanced OrderItem admin"""
    
    list_display = ('order', 'product', 'quantity', 'price_display', 'total_display')
    search_fields = ('product__title', 'order__user__email')
    list_filter = ('order__created_at',)
    
    @display(description="Price", ordering="price")
    def price_display(self, obj):
        return format_html('<strong>${}</strong>', obj.price)
    
    @display(description="Total")
    def total_display(self, obj):
        total = obj.price * obj.quantity
        return format_html('<strong style="color: green;">${}</strong>', total)


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    """Advanced Payment admin with status badges"""
    
    list_display = ('id', 'order', 'amount_display', 'method_badge', 'status_badge')
    search_fields = ('order__user__email', 'transaction_id')
    list_filter = ('status', 'method')
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    @display(description="Amount", ordering="amount")
    def amount_display(self, obj):
        return format_html('<strong style="color: green; font-size: 14px;">${}</strong>', obj.amount)
    
    @display(description="Method")
    def method_badge(self, obj):
        colors = {
            'card': '#4285f4',
            'paypal': '#00457c',
            'cash': '#34a853',
        }
        color = colors.get(obj.method, '#666')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.method.upper()
        )
    
    @display(description="Status")
    def status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'completed': '#4caf50',
            'failed': '#f44336',
        }
        color = colors.get(obj.status, '#666')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    
    @admin.action(description="Mark as completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} payments marked as completed")
    
    @admin.action(description="Mark as failed")
    def mark_as_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f"{queryset.count()} payments marked as failed")