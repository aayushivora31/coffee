from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    MenuItem, Cart, CartItem, Order, OrderItem, 
    Category, UserProfile, ContactMessage, DashboardAnalytics
)

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image_url', 'is_active', 'items_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_items_count(self, obj):
        return obj.menuitem_set.filter(is_available=True).count()

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for MenuItem model with image URL and pricing support
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    formatted_price = serializers.SerializerMethodField()
    image_url = serializers.URLField(allow_blank=True, allow_null=True)
    stock_status = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    category_obj = CategorySerializer(read_only=True)
    # Add category_obj_id field for easier editing
    category_obj_id = serializers.IntegerField(source='category_obj.id', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'formatted_price',
            'category', 'category_display', 'category_obj', 'category_obj_id', 'image_url', 'image',
            'stock', 'stock_status', 'is_in_stock', 'is_available', 'is_featured', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_formatted_price(self, obj):
        """
        Return formatted price with INR symbol
        """
        return f"₹{obj.price:.0f}"

class MenuItemListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for menu item lists (optimized for performance)
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    formatted_price = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'formatted_price',
            'category', 'category_display', 'image_url', 'stock', 'is_featured'
        ]
    
    def get_formatted_price(self, obj):
        return f"₹{obj.price:.0f}"

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem with menu item details
    """
    menu_item = MenuItemListSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'menu_item', 'menu_item_id', 'quantity',
            'total_price', 'formatted_total', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_total_price(self, obj):
        return obj.total_price
    
    def get_formatted_total(self, obj):
        return f"₹{obj.total_price:.0f}"

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart with items and totals
    """
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'items', 'total_items', 'total_price', 
            'formatted_total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_formatted_total(self, obj):
        return f"₹{obj.total_price:.0f}"

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem
    """
    menu_item = MenuItemListSerializer(read_only=True)
    formatted_price = serializers.SerializerMethodField()
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'menu_item', 'quantity', 'price', 
            'formatted_price', 'formatted_total'
        ]
    
    def get_formatted_price(self, obj):
        return f"₹{obj.price:.0f}"
    
    def get_formatted_total(self, obj):
        return f"₹{obj.total_price:.0f}"

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order with items
    """
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    formatted_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'customer_name', 'customer_email',
            'status', 'status_display', 'currency', 'currency_display',
            'total_amount', 'formatted_total', 'items', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_id', 'created_at', 'updated_at']
    
    def get_formatted_total(self, obj):
        currency_symbols = {'INR': '₹', 'GBP': '£', 'EUR': '€'}
        symbol = currency_symbols.get(obj.currency, '₹')
        return f"{symbol}{obj.total_amount:.0f}"

# Admin Dashboard Serializers
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (customers)"""
    full_name = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'is_active', 'date_joined', 'orders_count', 'total_spent'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_orders_count(self, obj):
        return obj.order_set.count()
    
    def get_total_spent(self, obj):
        from django.db.models import Sum
        total = obj.order_set.aggregate(total=Sum('total_amount'))['total'] or 0
        return f"₹{total:.0f}"

class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for Contact Messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class DashboardAnalyticsSerializer(serializers.Serializer):
    """Serializer for Dashboard Analytics"""
    total_orders = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    today_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    most_popular_item = serializers.DictField(allow_null=True)
    sales_data = serializers.ListField()
    category_stats = serializers.ListField()
    low_stock_items = serializers.ListField()
    recent_orders = OrderSerializer(many=True)

class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order status"""
    
    class Meta:
        model = Order
        fields = ['status', 'notes']
    
    def validate_status(self, value):
        allowed_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']
        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status")
        return value