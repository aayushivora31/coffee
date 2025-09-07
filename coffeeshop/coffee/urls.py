from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('auth/login/', views.login_view, name='login'),
    path('auth/signup/', views.signup_view, name='signup'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # Cart functionality
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Currency
    path('set-currency/', views.set_currency, name='set_currency'),
    
    # API
    path('api/messages/', views.api_messages, name='api_messages'),
    path('api/health/', views.api_health, name='api_health'),
    path('api/cart-count/', views.api_cart_count, name='api_cart_count'),
    
    # Menu API endpoints
    path('api/menu/', views.api_menu_items, name='api_menu_items'),
    path('api/menu/<int:item_id>/', views.api_menu_item_detail, name='api_menu_item_detail'),
    path('api/menu/categories/', views.api_menu_categories, name='api_menu_categories'),
    path('api/menu/featured/', views.api_featured_items, name='api_featured_items'),
    
    # Admin Dashboard
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', admin_views.admin_products, name='admin_products'),
    path('dashboard/orders/', admin_views.admin_orders, name='admin_orders'),
    path('dashboard/customers/', admin_views.admin_customers, name='admin_customers'),
    path('dashboard/messages/', admin_views.admin_messages, name='admin_messages'),
    path('dashboard/reports/', admin_views.admin_reports, name='admin_reports'),
    
    # Admin API endpoints
    path('api/admin/dashboard/analytics/', admin_views.dashboard_analytics, name='dashboard_analytics'),
    path('api/admin/products/', admin_views.admin_products_api, name='admin_products_api'),
    # Add URL pattern for individual product operations
    path('api/admin/products/<int:product_id>/', admin_views.admin_products_api, name='admin_product_detail_api'),
    path('api/admin/orders/', admin_views.admin_orders_api, name='admin_orders_api'),
    path('api/admin/customers/', admin_views.admin_customers_api, name='admin_customers_api'),
    path('api/admin/reports/', admin_views.admin_reports_api, name='admin_reports_api'),
    path('api/admin/messages/<int:message_id>/mark-read/', admin_views.mark_message_read_api, name='mark_message_read_api'),
    
    # Review and Rating System
    path('api/menu/<int:item_id>/reviews/', views.get_reviews, name='get_reviews'),
    path('api/menu/<int:item_id>/reviews/add/', views.add_review, name='add_review'),
    path('api/reviews/<int:review_id>/helpful/', views.mark_review_helpful, name='mark_review_helpful'),
    
    # Wishlist System
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('api/wishlist/add/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/wishlist/status/<int:item_id>/', views.get_wishlist_status, name='get_wishlist_status'),
    
    # Coupon System
    path('api/coupons/apply/', views.apply_coupon, name='apply_coupon'),
    
    # Search System
    path('search/', views.advanced_search, name='advanced_search'),
    path('api/search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/admin/categories/', admin_views.admin_categories_api, name='admin_categories_api'),
    path('api/admin/orders/stats/', admin_views.admin_orders_api, name='admin_orders_stats'),
    path('api/admin/customers/stats/', admin_views.admin_customers_api, name='admin_customers_stats'),
    path('api/admin/orders/<int:order_id>/', admin_views.admin_order_detail_api, name='admin_order_detail_api'),
    path('api/admin/customers/<int:customer_id>/', admin_views.admin_customer_detail_api, name='admin_customer_detail_api'),
]