import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
from .models import ContactMessage, MenuItem, Cart, CartItem, Order, OrderItem, UserProfile, Review, ReviewHelpful, Wishlist, WishlistItem, Coupon
from .forms import ContactForm, CustomUserCreationForm
from .signals import send_custom_form_notification
from django.utils import timezone

from django.templatetags.static import static
from django.utils.safestring import mark_safe

# Try to import Django REST Framework components
try:
    from .serializers import (
        MenuItemSerializer, MenuItemListSerializer, 
        CartSerializer, CartItemSerializer
    )
    DRF_AVAILABLE = True
except ImportError:
    DRF_AVAILABLE = False

# Image utility functions
def get_image_or_placeholder(image_url, placeholder_icon="bi-cup-hot", css_class=""):
    """Return image HTML or placeholder div"""
    if image_url:
        return mark_safe(f'<img src="{image_url}" class="{css_class}" alt="Menu Item" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'flex\'">')
    return mark_safe(f'<div class="placeholder-image {css_class}"><i class="{placeholder_icon}"></i></div>')

# Context processor for cart count
def cart_context(request):
    cart_count = 0
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        session_key = getattr(request.session, 'session_key', None) if hasattr(request, 'session') else None
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0
    
    return {'cart_count': cart_count}

def home(request):
    return render(request, 'coffee/home.html')

def about(request):
    return render(request, 'coffee/about.html')

def services(request):
    return render(request, 'coffee/services.html')

def menu(request):
    # Get all menu items grouped by category
    coffee_items = MenuItem.objects.filter(category='coffee', is_available=True)
    espresso_items = MenuItem.objects.filter(category='espresso', is_available=True)
    cold_drinks = MenuItem.objects.filter(category='cold_drinks', is_available=True)
    pastries = MenuItem.objects.filter(category='pastries', is_available=True)
    desserts = MenuItem.objects.filter(category='desserts', is_available=True)
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)
    
    # Get currency information
    currency = request.session.get('currency', 'GBP')
    currency_symbol = settings.CURRENCY_SYMBOLS.get(currency, '£')
    
    context = {
        'coffee_items': coffee_items,
        'espresso_items': espresso_items,
        'cold_drinks': cold_drinks,
        'pastries': pastries,
        'desserts': desserts,
        'featured_items': featured_items,
        'currency': currency,
        'currency_symbol': currency_symbol,
    }
    return render(request, 'coffee/menu.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            # The email notification will be sent via signal automatically to aayushivora31@gmail.com
            
            # Add enhanced logging for form submission
            logger.info(f'Contact form submitted by {contact_message.name} ({contact_message.email})')
            
            # Success message with more detail
            messages.success(request, f'Thank you {contact_message.name}! Your message has been sent successfully. We will get back to you soon at {contact_message.email}.')
            
            # Redirect to prevent resubmission
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = ContactForm()
    
    return render(request, 'coffee/contact.html', {'form': form})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_messages(request):
    if request.method == 'GET':
        messages_data = []
        for msg in ContactMessage.objects.all():
            messages_data.append({
                'id': msg.id,
                'name': msg.name,
                'email': msg.email,
                'message': msg.message,
                'created_at': msg.created_at.isoformat()
            })
        return JsonResponse(messages_data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            if not all(field in data for field in ['name', 'email', 'message']):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Create message
            message = ContactMessage.objects.create(
                name=data['name'],
                email=data['email'],
                message=data['message']
            )
            
            # Send additional custom form notification if this is from API
            form_data = {
                'name': data['name'],
                'email': data['email'],
                'message': data['message'],
                'submitted_at': timezone.now(),
                'submission_type': 'API Contact Form',
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
                'ip_address': request.META.get('REMOTE_ADDR', 'Unknown')
            }
            send_custom_form_notification('API Contact', form_data)
            
            return JsonResponse({
                'id': message.id,
                'name': message.name,
                'email': message.email,
                'message': message.message,
                'created_at': message.created_at.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def api_health(request):
    return JsonResponse({'status': 'ok'})

def api_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_count = cart.total_items
            except Cart.DoesNotExist:
                cart_count = 0
    
    return JsonResponse({'count': cart_count})

# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Send signup notification email to admin
            from .signals import send_notification_email
            signup_context = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
            }
            
            try:
                send_notification_email(
                    subject=f'New User Registration - {user.username}',
                    template_name='user_signup.html',
                    context=signup_context
                )
                logger.info(f'Signup notification sent for user: {user.username}')
            except Exception as e:
                logger.error(f'Failed to send signup notification: {str(e)}')
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'coffee/auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'coffee/auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')

# Cart Views
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        cart = get_or_create_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{menu_item.name} added to cart!')
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{menu_item.name} added to cart!',
                'cart_count': cart.total_items,
                'cart_total': str(cart.total_price)
            })
        
        return redirect('menu')
    
    return redirect('menu')

def cart_view(request):
    cart = get_or_create_cart(request)
    currency = request.session.get('currency', 'GBP')
    
    context = {
        'cart': cart,
        'currency': currency,
        'currency_symbol': settings.CURRENCY_SYMBOLS.get(currency, '£'),
    }
    return render(request, 'coffee/cart.html', context)

def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        currency = request.session.get('currency', 'GBP')
        order = Order.objects.create(
            user=request.user,
            customer_name=request.user.get_full_name() or request.user.username,
            customer_email=request.user.email,
            currency=currency,
            total_amount=cart.total_price,
            notes=request.POST.get('notes', '')
        )
        
        # Create order items
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price
            )
        
        # Clear cart
        cart.cartitem_set.all().delete()
        
        messages.success(request, f'Your order #{order.order_id} has been placed successfully!')
        return redirect('order_confirmation', order_id=order.order_id)
    
    currency = request.session.get('currency', 'GBP')
    context = {
        'cart': cart,
        'currency': currency,
        'currency_symbol': settings.CURRENCY_SYMBOLS.get(currency, '£'),
    }
    return render(request, 'coffee/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    context = {
        'order': order,
        'currency_symbol': settings.CURRENCY_SYMBOLS.get(order.currency, '₹'),
    }
    return render(request, 'coffee/order_confirmation.html', context)

# Currency Views
def set_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('currency', 'GBP')
        if currency in settings.CURRENCY_SYMBOLS:
            request.session['currency'] = currency
            messages.success(request, f'Currency changed to {currency}')
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Helper function to convert prices
def convert_price(price, from_currency='GBP', to_currency='GBP'):
    if from_currency == to_currency:
        return price
    
    gbp_price = price / Decimal(str(settings.CURRENCY_RATES[from_currency]))
    converted_price = gbp_price * Decimal(str(settings.CURRENCY_RATES[to_currency]))
    return round(converted_price, 2)

# ============================================================================
# API ENDPOINTS FOR MENU ITEMS
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def api_menu_items(request):
    """
    API endpoint to get all menu items with pagination and filtering
    """
    try:
        # Get query parameters
        category = request.GET.get('category')
        search = request.GET.get('search')
        featured = request.GET.get('featured')
        page = request.GET.get('page', 1)
        per_page = min(int(request.GET.get('per_page', 20)), 100)  # Max 100 items per page
        
        # Build queryset
        queryset = MenuItem.objects.filter(is_available=True)
        
        if category:
            queryset = queryset.filter(category=category)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Paginate
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize data
        if DRF_AVAILABLE:
            serializer = MenuItemListSerializer(page_obj.object_list, many=True)
            items = serializer.data
        else:
            # Fallback manual serialization
            items = []
            for item in page_obj.object_list:
                items.append({
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'formatted_price': f"£{item.price:.2f}",
                    'category': item.category,
                    'category_display': item.get_category_display(),
                    'image_url': item.image_url,
                    'is_featured': item.is_featured
                })
        
        return JsonResponse({
            'items': items,
            'pagination': {
                'page': page_obj.number,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            },
            'categories': list(MenuItem.CATEGORY_CHOICES)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def api_menu_item_detail(request, item_id):
    """
    API endpoint to get a specific menu item
    """
    try:
        item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        
        if DRF_AVAILABLE:
            serializer = MenuItemSerializer(item)
            return JsonResponse(serializer.data)
        else:
            # Fallback manual serialization
            return JsonResponse({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'formatted_price': f"₹{item.price:.0f}",
                'category': item.category,
                'category_display': item.get_category_display(),
                'image_url': item.image_url,
                'is_available': item.is_available,
                'is_featured': item.is_featured,
                'created_at': item.created_at.isoformat(),
                'updated_at': item.updated_at.isoformat()
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

@csrf_exempt
@require_http_methods(["GET"])
def api_menu_categories(request):
    """
    API endpoint to get menu items grouped by category
    """
    try:
        categories_data = {}
        
        for category_code, category_name in MenuItem.CATEGORY_CHOICES:
            items = MenuItem.objects.filter(category=category_code, is_available=True)
            
            if DRF_AVAILABLE:
                serializer = MenuItemListSerializer(items, many=True)
                items_data = serializer.data
            else:
                # Fallback manual serialization
                items_data = []
                for item in items:
                    items_data.append({
                        'id': item.id,
                        'name': item.name,
                        'description': item.description,
                        'price': float(item.price),
                        'formatted_price': f"£{item.price:.2f}",
                        'image_url': item.image_url,
                        'is_featured': item.is_featured
                    })
            
            categories_data[category_code] = {
                'name': category_name,
                'items': items_data,
                'count': len(items_data)
            }
        
        return JsonResponse({
            'categories': categories_data,
            'total_categories': len(categories_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def api_featured_items(request):
    """
    API endpoint to get featured menu items
    """
    try:
        featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)
        
        if DRF_AVAILABLE:
            serializer = MenuItemListSerializer(featured_items, many=True)
            items_data = serializer.data
        else:
            # Fallback manual serialization
            items_data = []
            for item in featured_items:
                items_data.append({
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),
                    'formatted_price': f"£{item.price:.2f}",
                    'category': item.category,
                    'category_display': item.get_category_display(),
                    'image_url': item.image_url,
                    'is_featured': item.is_featured
                })
        
        return JsonResponse({
            'featured_items': items_data,
            'count': len(items_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ============================================================================
# REVIEW AND RATING SYSTEM
# ============================================================================

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_review(request, item_id):
    """Add a review for a menu item"""
    try:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        # Check if user already reviewed this item
        if Review.objects.filter(menu_item=menu_item, user=request.user).exists():
            return JsonResponse({'error': 'You have already reviewed this item'}, status=400)
        
        data = json.loads(request.body)
        rating = int(data.get('rating', 0))
        title = data.get('title', '').strip()
        comment = data.get('comment', '').strip()
        
        # Validate input
        if not (1 <= rating <= 5):
            return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        if not title:
            return JsonResponse({'error': 'Review title is required'}, status=400)
        if not comment:
            return JsonResponse({'error': 'Review comment is required'}, status=400)
        
        # Create review
        review = Review.objects.create(
            menu_item=menu_item,
            user=request.user,
            rating=rating,
            title=title,
            comment=comment
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Review added successfully',
            'review': {
                'id': review.id,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'user': review.user.username,
                'created_at': review.created_at.isoformat(),
                'star_display': review.star_display
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_reviews(request, item_id):
    """Get all reviews for a menu item"""
    try:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        reviews = menu_item.reviews.all().order_by('-created_at')
        
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'id': review.id,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'user': review.user.username,
                'created_at': review.created_at.isoformat(),
                'star_display': review.star_display,
                'helpful_count': review.helpful_count,
                'is_verified': review.is_verified
            })
        
        return JsonResponse({
            'reviews': reviews_data,
            'average_rating': menu_item.average_rating,
            'rating_count': menu_item.rating_count,
            'rating_breakdown': menu_item.get_rating_breakdown()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_review_helpful(request, review_id):
    """Mark a review as helpful"""
    try:
        review = get_object_or_404(Review, id=review_id)
        
        # Check if user already marked this review as helpful
        helpful_vote, created = ReviewHelpful.objects.get_or_create(
            review=review,
            user=request.user
        )
        
        if created:
            review.helpful_count += 1
            review.save()
            return JsonResponse({
                'success': True,
                'message': 'Review marked as helpful',
                'helpful_count': review.helpful_count
            })
        else:
            # Remove helpful vote
            helpful_vote.delete()
            review.helpful_count = max(0, review.helpful_count - 1)
            review.save()
            return JsonResponse({
                'success': True,
                'message': 'Helpful vote removed',
                'helpful_count': review.helpful_count
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# WISHLIST FUNCTIONALITY
# ============================================================================

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_to_wishlist(request, item_id):
    """Add item to user's wishlist"""
    try:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        # Get or create wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Check if item already in wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            menu_item=menu_item
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': 'Item added to wishlist',
                'in_wishlist': True
            })
        else:
            # Remove from wishlist
            wishlist_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from wishlist',
                'in_wishlist': False
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.items.all().select_related('menu_item')
    except Wishlist.DoesNotExist:
        wishlist_items = []
    
    # Get currency information
    currency = request.session.get('currency', 'GBP')
    currency_symbol = settings.CURRENCY_SYMBOLS.get(currency, '£')
    
    context = {
        'wishlist_items': wishlist_items,
        'currency': currency,
        'currency_symbol': currency_symbol,
    }
    return render(request, 'coffee/wishlist.html', context)


@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_wishlist_status(request, item_id):
    """Check if item is in user's wishlist"""
    try:
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            in_wishlist = WishlistItem.objects.filter(
                wishlist=wishlist,
                menu_item=menu_item
            ).exists()
        except Wishlist.DoesNotExist:
            in_wishlist = False
        
        return JsonResponse({'in_wishlist': in_wishlist})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# COUPON SYSTEM
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def apply_coupon(request):
    """Apply coupon code to get discount"""
    try:
        data = json.loads(request.body)
        coupon_code = data.get('code', '').strip().upper()
        order_total = Decimal(str(data.get('total', 0)))
        
        if not coupon_code:
            return JsonResponse({'error': 'Coupon code is required'}, status=400)
        
        # Find coupon
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'error': 'Invalid coupon code'}, status=400)
        
        # Check if coupon is valid
        if not coupon.is_valid:
            return JsonResponse({'error': 'This coupon has expired or is no longer valid'}, status=400)
        
        # Calculate discount
        discount_amount = coupon.calculate_discount(order_total)
        
        if discount_amount <= 0:
            return JsonResponse({
                'error': f'Order total must be at least ₹{coupon.minimum_amount} to use this coupon'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'coupon': {
                'code': coupon.code,
                'name': coupon.name,
                'description': coupon.description,
                'discount_amount': float(discount_amount),
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value)
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# ADVANCED SEARCH AND FILTERING SYSTEM
# ============================================================================

def advanced_search(request):
    """Advanced search page with filters"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort', 'name')
    
    # Build queryset
    items = MenuItem.objects.filter(is_available=True)
    
    # Search filter
    if query:
        items = items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Category filter
    if category:
        items = items.filter(category=category)
    
    # Price filters
    if min_price:
        try:
            items = items.filter(price__gte=Decimal(min_price))
        except:
            pass
    
    if max_price:
        try:
            items = items.filter(price__lte=Decimal(max_price))
        except:
            pass
    
    # Sorting
    if sort_by == 'price_low':
        items = items.order_by('price')
    elif sort_by == 'price_high':
        items = items.order_by('-price')
    elif sort_by == 'rating':
        items = items.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')
    elif sort_by == 'popular':
        items = items.annotate(order_count=models.Count('orderitem')).order_by('-order_count')
    else:
        items = items.order_by('name')
    
    # Pagination
    paginator = Paginator(items, 12)
    page = request.GET.get('page', 1)
    items_page = paginator.get_page(page)
    
    # Get categories for filter dropdown
    categories = MenuItem.CATEGORY_CHOICES
    
    # Get currency information
    currency = request.session.get('currency', 'GBP')
    currency_symbol = settings.CURRENCY_SYMBOLS.get(currency, '£')
    
    context = {
        'items': items_page,
        'query': query,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'categories': categories,
        'currency': currency,
        'currency_symbol': currency_symbol,
        'total_results': paginator.count
    }
    
    return render(request, 'coffee/search.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def search_suggestions(request):
    """Get search suggestions for autocomplete"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get matching items
    items = MenuItem.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_available=True
    )[:8]
    
    suggestions = []
    for item in items:
        suggestions.append({
            'id': item.id,
            'name': item.name,
            'category': item.get_category_display(),
            'price': float(item.price)
        })
    
    return JsonResponse({'suggestions': suggestions})
