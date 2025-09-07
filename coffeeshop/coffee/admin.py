from django.contrib import admin
from .models import ContactMessage, MenuItem, Cart, CartItem, Order, OrderItem, UserProfile

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'is_featured')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message_preview', 'is_read', 'created_at')
    list_filter = ('created_at', 'is_read')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def total_items(self, obj):
        return obj.total_items
    
    def total_price(self, obj):
        return f"${obj.total_price}"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'menu_item', 'quantity', 'total_price']
    list_filter = ['created_at']
    
    def total_price(self, obj):
        return f"${obj.total_price}"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'status', 'currency', 'total_amount', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_email']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    list_editable = ['status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price', 'total_price']
    list_filter = ['order__created_at']
    
    def total_price(self, obj):
        return f"${obj.total_price}"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'preferred_currency', 'created_at']
    list_filter = ['preferred_currency', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
