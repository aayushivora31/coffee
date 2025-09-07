from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum, Count
from decimal import Decimal
import uuid

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'Coffee'),
        ('espresso', 'Espresso'),
        ('cold_drinks', 'Cold Drinks'),
        ('pastries', 'Pastries'),
        ('sandwiches', 'Sandwiches'),
        ('desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='coffee')
    category_obj = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10, help_text="Available stock quantity")
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - £{self.price}"
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    @property
    def stock_status(self):
        if self.stock == 0:
            return "Out of Stock"
        elif self.stock <= 5:
            return "Low Stock"
        else:
            return "In Stock"
    
    def reduce_stock(self, quantity):
        """Reduce stock when item is ordered"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        return 0
    
    @property
    def rating_count(self):
        """Get total number of reviews"""
        return self.reviews.count()
    
    @property
    def star_display(self):
        """Return star rating display for templates"""
        avg_rating = self.average_rating
        full_stars = int(avg_rating)
        half_star = 1 if avg_rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        return {
            'full_stars': range(full_stars),
            'half_star': half_star,
            'empty_stars': range(empty_stars),
            'rating': round(avg_rating, 1)
        }
    
    def get_rating_breakdown(self):
        """Get rating breakdown (1-5 stars count)"""
        breakdown = {i: 0 for i in range(1, 6)}
        reviews = self.reviews.all()
        for review in reviews:
            breakdown[review.rating] += 1
        return breakdown
    
    class Meta:
        ordering = ['category', 'name']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous Cart {self.session_key[:8]}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.cartitem_set.all())
    
    class Meta:
        ordering = ['-updated_at']

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.menu_item.price
    
    class Meta:
        unique_together = ['cart', 'menu_item']
        ordering = ['-created_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (₹)'),
        ('GBP', 'British Pound (£)'),
        ('EUR', 'Euro (€)'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order {self.order.order_id})"
    
    @property
    def total_price(self):
        return self.quantity * self.price

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    preferred_currency = models.CharField(max_length=3, choices=Order.CURRENCY_CHOICES, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']

# Dashboard Analytics Models
class DashboardAnalytics(models.Model):
    """Helper model for dashboard analytics"""
    
    @classmethod
    def get_total_orders(cls):
        return Order.objects.count()
    
    @classmethod
    def get_total_customers(cls):
        return User.objects.filter(is_staff=False).count()
    
    @classmethod
    def get_today_revenue(cls):
        today = timezone.now().date()
        orders = Order.objects.filter(
            created_at__date=today,
            status__in=['delivered', 'ready']
        )
        return orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    @classmethod
    def get_most_popular_item(cls):
        popular = OrderItem.objects.values('menu_item__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity').first()
        
        if popular:
            return {
                'name': popular['menu_item__name'],
                'quantity': popular['total_quantity']
            }
        return None
    
    @classmethod
    def get_sales_data(cls, days=7):
        """Get sales data for last N days"""
        from datetime import timedelta
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        sales_data = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            orders = Order.objects.filter(
                created_at__date=date,
                status__in=['delivered', 'ready']
            )
            revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'revenue': float(revenue),
                'orders': orders.count()
            })
        
        return sales_data
    
    @classmethod
    def get_category_stats(cls):
        """Get sales statistics by category"""
        category_stats = OrderItem.objects.values(
            'menu_item__category'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(models.F('quantity') * models.F('price'))
        ).order_by('-total_revenue')
        
        return list(category_stats)
    
    class Meta:
        managed = False  # This is a utility model, no database table needed


# Review and Rating System
class Review(models.Model):
    """Product review model with star ratings"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)  # For verified purchases
    helpful_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('menu_item', 'user')  # One review per user per item
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.menu_item.name} ({self.rating} stars)'
    
    @property
    def star_display(self):
        """Return star rating as HTML"""
        stars = '★' * self.rating + '☆' * (5 - self.rating)
        return stars


class ReviewHelpful(models.Model):
    """Track helpful review votes"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('review', 'user')


# Wishlist System
class Wishlist(models.Model):
    """User wishlist for favorite items"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist"
    
    @property
    def total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """Individual wishlist items"""
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('wishlist', 'menu_item')
    
    def __str__(self):
        return f"{self.menu_item.name} in {self.wishlist.user.username}'s wishlist"


# Coupon and Discount System
class Coupon(models.Model):
    """Discount coupons and promo codes"""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('free_shipping', 'Free Shipping'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        """Check if coupon is currently valid"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def calculate_discount(self, amount):
        """Calculate discount amount for given order total"""
        if not self.is_valid or amount < self.minimum_amount:
            return 0
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
        elif self.discount_type == 'fixed':
            discount = min(self.discount_value, amount)
        else:  # free_shipping
            discount = 0  # Handled separately in shipping calculation
        
        return discount


class CouponUsage(models.Model):
    """Track coupon usage by users"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.coupon.code} used by {self.user.username}"
