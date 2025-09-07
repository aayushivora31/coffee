# Try to import Django REST Framework components
try:
    from rest_framework import viewsets, status
    from rest_framework.decorators import action, api_view, permission_classes
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated, IsAdminUser
    from .serializers import (
        MenuItemSerializer, CategorySerializer, OrderSerializer, 
        UserSerializer, ContactMessageSerializer, DashboardAnalyticsSerializer,
        OrderUpdateSerializer
    )
    DRF_AVAILABLE = True
except ImportError:
    DRF_AVAILABLE = False
    # Define dummy decorators for when DRF is not available
    def api_view(methods):
        def decorator(func):
            return func
        return decorator
    
    def permission_classes(perms):
        def decorator(func):
            return func
        return decorator

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db import models

from .models import (
    MenuItem, Category, Order, OrderItem, 
    ContactMessage, DashboardAnalytics
)


# Django REST Framework ViewSets (only available when DRF is installed)
if DRF_AVAILABLE:
    class AdminDashboardViewSet(viewsets.ViewSet):
        """Admin Dashboard API ViewSet"""
        permission_classes = [IsAdminUser]
        
        @action(detail=False, methods=['get'])
        def analytics(self, request):
            """Get dashboard analytics data"""
            try:
                # Get basic metrics
                total_orders = DashboardAnalytics.get_total_orders()
                total_customers = DashboardAnalytics.get_total_customers()
                today_revenue = DashboardAnalytics.get_today_revenue()
                most_popular_item = DashboardAnalytics.get_most_popular_item()
                
                # Get sales data for charts
                days = int(request.query_params.get('days', 7))
                sales_data = DashboardAnalytics.get_sales_data(days)
                category_stats = DashboardAnalytics.get_category_stats()
                
                # Get low stock items
                low_stock_items = MenuItem.objects.filter(
                    stock__lte=5, is_available=True
                ).values('id', 'name', 'stock', 'category')
                
                # Get recent orders
                recent_orders = Order.objects.select_related('user').prefetch_related(
                    'orderitem_set__menu_item'
                ).order_by('-created_at')[:10]
                
                analytics_data = {
                    'total_orders': total_orders,
                    'total_customers': total_customers,
                    'today_revenue': today_revenue,
                    'most_popular_item': most_popular_item,
                    'sales_data': sales_data,
                    'category_stats': category_stats,
                    'low_stock_items': list(low_stock_items),
                    'recent_orders': OrderSerializer(recent_orders, many=True).data
                }
                
                serializer = DashboardAnalyticsSerializer(analytics_data)
                return Response(serializer.data)
                
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


    class MenuItemAdminViewSet(viewsets.ModelViewSet):
        """Admin ViewSet for MenuItem management"""
        queryset = MenuItem.objects.all().order_by('-created_at')
        serializer_class = MenuItemSerializer
        permission_classes = [IsAdminUser]
        
        def get_queryset(self):
            queryset = super().get_queryset()
            category = self.request.query_params.get('category')
            stock_status = self.request.query_params.get('stock_status')
            search = self.request.query_params.get('search')
            
            if category:
                queryset = queryset.filter(category=category)
            
            if stock_status == 'low':
                queryset = queryset.filter(stock__lte=5)
            elif stock_status == 'out':
                queryset = queryset.filter(stock=0)
            
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | 
                    Q(description__icontains=search)
                )
            
            return queryset
        
        @action(detail=True, methods=['post'])
        def update_stock(self, request, pk=None):
            """Update stock for a menu item"""
            menu_item = self.get_object()
            new_stock = request.data.get('stock')
            
            if new_stock is not None:
                try:
                    menu_item.stock = int(new_stock)
                    menu_item.save()
                    
                    return Response({
                        'success': True,
                        'message': f'Stock updated to {new_stock}',
                        'stock': menu_item.stock,
                        'stock_status': menu_item.stock_status
                    })
                except ValueError:
                    return Response(
                        {'error': 'Invalid stock value'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            return Response(
                {'error': 'Stock value required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


    class OrderAdminViewSet(viewsets.ModelViewSet):
        """Admin ViewSet for Order management"""
        queryset = Order.objects.all().order_by('-created_at')
        serializer_class = OrderSerializer
        permission_classes = [IsAdminUser]
        
        def get_queryset(self):
            queryset = super().get_queryset()
            status_filter = self.request.query_params.get('status')
            date_from = self.request.query_params.get('date_from')
            date_to = self.request.query_params.get('date_to')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if date_from:
                queryset = queryset.filter(created_at__date__gte=date_from)
            
            if date_to:
                queryset = queryset.filter(created_at__date__lte=date_to)
            
            return queryset
        
        @action(detail=True, methods=['patch'])
        def update_status(self, request, pk=None):
            """Update order status"""
            order = self.get_object()
            serializer = OrderUpdateSerializer(order, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': f'Order status updated to {order.get_status_display()}',
                    'order': OrderSerializer(order).data
                })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    class CustomerAdminViewSet(viewsets.ReadOnlyModelViewSet):
        """Admin ViewSet for Customer management"""
        queryset = User.objects.filter(is_staff=False).order_by('-date_joined')
        serializer_class = UserSerializer
        permission_classes = [IsAdminUser]
        
        def get_queryset(self):
            queryset = super().get_queryset()
            search = self.request.query_params.get('search')
            
            if search:
                queryset = queryset.filter(
                    Q(username__icontains=search) |
                    Q(email__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                )
            
            return queryset


    class CategoryAdminViewSet(viewsets.ModelViewSet):
        """Admin ViewSet for Category management"""
        queryset = Category.objects.all().order_by('name')
        serializer_class = CategorySerializer
        permission_classes = [IsAdminUser]


    class ContactMessageAdminViewSet(viewsets.ModelViewSet):
        """Admin ViewSet for Contact Message management"""
        queryset = ContactMessage.objects.all().order_by('-created_at')
        serializer_class = ContactMessageSerializer
        permission_classes = [IsAdminUser]
        
        @action(detail=True, methods=['post'])
        def mark_read(self, request, pk=None):
            """Mark contact message as read"""
            message = self.get_object()
            message.is_read = True
            message.save()
            
            return Response({
                'success': True,
                'message': 'Message marked as read'
            })


# Dashboard Template Views
@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard view"""
    context = {
        'page_title': 'Admin Dashboard',
        'total_orders': DashboardAnalytics.get_total_orders(),
        'total_customers': DashboardAnalytics.get_total_customers(),
        'today_revenue': DashboardAnalytics.get_today_revenue(),
        'most_popular_item': DashboardAnalytics.get_most_popular_item(),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@staff_member_required
def admin_products(request):
    """Products management view"""
    products = MenuItem.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'page_title': 'Product Management',
        'products': products,
        'categories': categories,
    }
    return render(request, 'admin_dashboard/products.html', context)


@staff_member_required
def admin_orders(request):
    """Orders management view"""
    orders = Order.objects.all().order_by('-created_at')[:50]
    
    context = {
        'page_title': 'Order Management',
        'orders': orders,
    }
    return render(request, 'admin_dashboard/orders.html', context)


@staff_member_required
def admin_customers(request):
    """Customers management view"""
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')[:50]
    
    context = {
        'page_title': 'Customer Management',
        'customers': customers,
    }
    return render(request, 'admin_dashboard/customers.html', context)


@staff_member_required
def admin_reports(request):
    """Reports and analytics view"""
    context = {
        'page_title': 'Reports & Analytics',
        'sales_data': DashboardAnalytics.get_sales_data(30),
        'category_stats': DashboardAnalytics.get_category_stats(),
    }
    return render(request, 'admin_dashboard/reports.html', context)


@staff_member_required
def admin_messages(request):
    """Contact Messages management view"""
    messages_queryset = ContactMessage.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        messages_queryset = messages_queryset.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    # Filter by read status
    status_filter = request.GET.get('status', '')
    if status_filter == 'unread':
        messages_queryset = messages_queryset.filter(is_read=False)
    elif status_filter == 'read':
        messages_queryset = messages_queryset.filter(is_read=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(messages_queryset, 20)  # Show 20 messages per page
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    # Statistics
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    today_messages = ContactMessage.objects.filter(created_at__date=timezone.now().date()).count()
    
    context = {
        'page_title': 'Contact Messages',
        'messages': messages_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'today_messages': today_messages,
    }
    return render(request, 'admin_dashboard/messages.html', context)


# API Views for Dashboard
@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics"""
    stats = {
        'total_orders': DashboardAnalytics.get_total_orders(),
        'total_customers': DashboardAnalytics.get_total_customers(),
        'today_revenue': float(DashboardAnalytics.get_today_revenue()),
        'most_popular_item': DashboardAnalytics.get_most_popular_item(),
        'low_stock_count': MenuItem.objects.filter(stock__lte=5).count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_chart_api(request):
    """API endpoint for sales chart data"""
    days = int(request.GET.get('days', 7))
    sales_data = DashboardAnalytics.get_sales_data(days)
    
    return Response({
        'sales_data': sales_data,
        'category_stats': DashboardAnalytics.get_category_stats()
    })


# Admin API endpoints - modified to work with or without DRF
@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def dashboard_analytics(request):
    """Dashboard analytics API endpoint"""
    try:
        # Get basic metrics
        total_orders = DashboardAnalytics.get_total_orders()
        total_customers = DashboardAnalytics.get_total_customers()
        today_revenue = DashboardAnalytics.get_today_revenue()
        most_popular_item = DashboardAnalytics.get_most_popular_item()
        
        # Get sales data for charts
        days = int(request.GET.get('days', 7))
        sales_data = DashboardAnalytics.get_sales_data(days)
        category_stats = DashboardAnalytics.get_category_stats()
        
        # Get low stock items
        low_stock_items = MenuItem.objects.filter(
            stock__lte=5, is_available=True
        ).values('id', 'name', 'stock', 'category')
        
        # Get recent orders
        recent_orders = Order.objects.select_related('user').prefetch_related(
            'orderitem_set__menu_item'
        ).order_by('-created_at')[:10]
        
        analytics_data = {
            'total_orders': total_orders,
            'total_customers': total_customers,
            'today_revenue': float(today_revenue),
            'most_popular_item': most_popular_item,
            'sales_data': sales_data,
            'category_stats': list(category_stats),
            'low_stock_items': list(low_stock_items),
            'recent_orders': [{
                'id': order.id,
                'order_id': str(order.order_id),
                'customer_name': order.customer_name,
                'total_amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat()
            } for order in recent_orders]
        }
        
        if DRF_AVAILABLE:
            return Response(analytics_data)
        else:
            return JsonResponse(analytics_data)
            
    except Exception as e:
        error_response = {'error': str(e)}
        if DRF_AVAILABLE:
            return Response(error_response, status=500)
        else:
            return JsonResponse(error_response, status=500)


@api_view(['GET', 'POST', 'PUT', 'DELETE']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_products_api(request, product_id=None):
    """Products API endpoint"""
    if request.method == 'GET':
        try:
            products = MenuItem.objects.all().order_by('-created_at')
            products_data = []
            for product in products:
                if DRF_AVAILABLE:
                    product_data = MenuItemSerializer(product).data
                else:
                    product_data = {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': float(product.price),
                        'category': product.category,
                        'image_url': product.image_url,
                        'stock': product.stock,
                        'is_available': product.is_available,
                        'is_featured': product.is_featured,
                        'created_at': product.created_at.isoformat() if product.created_at else None
                    }
                product_data['category_name'] = product.category_obj.name if product.category_obj else None
                # Add category_obj ID for editing
                product_data['category_obj'] = product.category_obj.id if product.category_obj else None
                product_data['category_obj_id'] = product.category_obj.id if product.category_obj else None
                products_data.append(product_data)
            
            if DRF_AVAILABLE:
                return Response(products_data)
            else:
                return JsonResponse(products_data, safe=False)
        except Exception as e:
            # Log the actual error for debugging
            import logging
            logging.error(f"Error fetching products: {str(e)}")
            error_response = {'error': f'Error fetching products: {str(e)}'}
            if DRF_AVAILABLE:
                return Response(error_response, status=500)
            else:
                return JsonResponse(error_response, status=500)
    
    elif request.method == 'POST':
        if DRF_AVAILABLE:
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                # Handle category_obj assignment
                category_id = request.data.get('category')
                if category_id:
                    try:
                        category = Category.objects.get(id=category_id)
                        serializer.save(category_obj=category)
                    except Category.DoesNotExist:
                        return Response({'error': 'Invalid category'}, status=400)
                else:
                    serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            # Handle without DRF
            try:
                # Check if request has FILES (FormData with file upload)
                if request.content_type and 'multipart/form-data' in request.content_type:
                    # Handle FormData with file uploads
                    # Create product fields from POST data
                    name = request.POST.get('name')
                    if not name:
                        return JsonResponse({'error': 'Product name is required'}, status=400)
                        
                    description = request.POST.get('description', '')
                    price = request.POST.get('price')
                    if not price:
                        return JsonResponse({'error': 'Price is required'}, status=400)
                    
                    try:
                        price = float(price)
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Invalid price format'}, status=400)
                        
                    stock = request.POST.get('stock', 10)
                    try:
                        stock = int(stock)
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Invalid stock format'}, status=400)
                        
                    is_available = request.POST.get('is_available')
                    is_featured = request.POST.get('is_featured')
                    
                    # Handle category_obj
                    category_id = request.POST.get('category')
                    category_obj = None
                    if category_id:
                        try:
                            category_obj = Category.objects.get(id=category_id)
                        except Category.DoesNotExist:
                            return JsonResponse({'error': 'Invalid category'}, status=400)
                    
                    # Handle image upload if provided
                    image = None
                    if 'image' in request.FILES:
                        image = request.FILES['image']
                    
                    product = MenuItem.objects.create(
                        name=name,
                        description=description,
                        price=price,
                        category_obj=category_obj,
                        image=image,
                        stock=stock,
                        is_available=is_available in ['on', 'true', '1'],
                        is_featured=is_featured in ['on', 'true', '1']
                    )
                else:
                    # Handle JSON data (for API calls)
                    import json
                    try:
                        data = json.loads(request.body)
                    except json.JSONDecodeError:
                        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
                        
                    # Validate required fields
                    if not data.get('name'):
                        return JsonResponse({'error': 'Product name is required'}, status=400)
                        
                    if not data.get('price'):
                        return JsonResponse({'error': 'Price is required'}, status=400)
                    
                    try:
                        price = float(data['price'])
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Invalid price format'}, status=400)
                        
                    stock = data.get('stock', 10)
                    try:
                        stock = int(stock)
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Invalid stock format'}, status=400)
                    
                    product = MenuItem.objects.create(
                        name=data.get('name'),
                        description=data.get('description', ''),
                        price=price,
                        # Use category_obj instead of category for the new system
                        category_obj_id=data.get('category') if data.get('category') else None,
                        image_url=data.get('image_url'),
                        stock=stock,
                        is_available=data.get('is_available', True),
                        is_featured=data.get('is_featured', False)
                    )
                return JsonResponse({
                    'id': product.id,
                    'name': product.name,
                    'message': 'Product created successfully'
                }, status=201)
            except Exception as e:
                # Log the actual error for debugging
                import logging
                logging.error(f"Error creating product: {str(e)}")
                return JsonResponse({'error': f'Error creating product: {str(e)}'}, status=400)
    
    elif request.method == 'PUT':
        if not product_id:
            error_response = {'error': 'Product ID required'}
            if DRF_AVAILABLE:
                return Response(error_response, status=400)
            else:
                return JsonResponse(error_response, status=400)
            
        try:
            product = MenuItem.objects.get(id=product_id)
        except MenuItem.DoesNotExist:
            error_response = {'error': 'Product not found'}
            if DRF_AVAILABLE:
                return Response(error_response, status=404)
            else:
                return JsonResponse(error_response, status=404)
        
        if DRF_AVAILABLE:
            # For DRF, we need to handle the update properly with partial=True
            serializer = MenuItemSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                # Handle category_obj assignment
                category_id = request.data.get('category')
                if category_id:
                    try:
                        category = Category.objects.get(id=category_id)
                        serializer.save(category_obj=category)
                    except Category.DoesNotExist:
                        return Response({'error': 'Invalid category'}, status=400)
                else:
                    serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            # Handle without DRF - properly handle FormData
            try:
                # Check if request has FILES (FormData with file upload)
                if request.content_type and 'multipart/form-data' in request.content_type:
                    # Handle FormData with file uploads
                    # Update product fields from POST data
                    name = request.POST.get('name')
                    if name is not None:
                        product.name = name
                        
                    description = request.POST.get('description')
                    if description is not None:
                        product.description = description
                        
                    price = request.POST.get('price')
                    if price is not None:
                        try:
                            product.price = price
                        except (ValueError, TypeError):
                            return JsonResponse({'error': 'Invalid price format'}, status=400)
                        
                    stock = request.POST.get('stock')
                    if stock is not None:
                        try:
                            product.stock = int(stock)
                        except (ValueError, TypeError):
                            return JsonResponse({'error': 'Invalid stock format'}, status=400)
                        
                    is_available = request.POST.get('is_available')
                    # Checkbox handling - if not present, it's unchecked
                    product.is_available = is_available in ['on', 'true', '1']
                    
                    is_featured = request.POST.get('is_featured')
                    if is_featured is not None:
                        product.is_featured = is_featured in ['on', 'true', '1']
                    
                    # Handle category_obj
                    category_id = request.POST.get('category')
                    if category_id:
                        try:
                            category = Category.objects.get(id=category_id)
                            product.category_obj = category
                        except Category.DoesNotExist:
                            return JsonResponse({'error': 'Invalid category'}, status=400)
                    else:
                        product.category_obj = None
                    
                    # Handle image upload if provided
                    if 'image' in request.FILES:
                        product.image = request.FILES['image']
                        
                else:
                    # Handle JSON data (for API calls)
                    import json
                    try:
                        data = json.loads(request.body)
                    except json.JSONDecodeError:
                        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
                    
                    # Update product fields
                    for field in ['name', 'description']:
                        if field in data:
                            setattr(product, field, data[field])
                    
                    # Handle numeric fields with validation
                    if 'price' in data:
                        try:
                            product.price = data['price']
                        except (ValueError, TypeError):
                            return JsonResponse({'error': 'Invalid price format'}, status=400)
                    
                    if 'stock' in data:
                        try:
                            product.stock = int(data['stock'])
                        except (ValueError, TypeError):
                            return JsonResponse({'error': 'Invalid stock format'}, status=400)
                    
                    # Handle boolean fields
                    if 'is_available' in data:
                        product.is_available = data['is_available'] in [True, False] and data['is_available']
                    
                    if 'is_featured' in data:
                        product.is_featured = data['is_featured'] in [True, False] and data['is_featured']
                    
                    # Handle category_obj
                    if 'category' in data:
                        if data['category']:
                            try:
                                category = Category.objects.get(id=data['category'])
                                product.category_obj = category
                            except Category.DoesNotExist:
                                return JsonResponse({'error': 'Invalid category'}, status=400)
                        else:
                            product.category_obj = None
                
                product.save()
                return JsonResponse({
                    'id': product.id,
                    'name': product.name,
                    'message': 'Product updated successfully'
                })
            except Exception as e:
                # Log the actual error for debugging
                import logging
                logging.error(f"Error updating product: {str(e)}")
                return JsonResponse({'error': f'Error updating product: {str(e)}'}, status=400)
    
    elif request.method == 'DELETE':
        if not product_id:
            return Response({'error': 'Product ID required'}, status=400)
            
        try:
            product = MenuItem.objects.get(id=product_id)
            product.delete()
            return Response({'message': 'Product deleted successfully'})
        except MenuItem.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_orders_api(request):
    """Orders API endpoint"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Get order stats
    if request.path.endswith('/stats/'):
        stats = {}
        for status_choice in ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']:
            stats[status_choice] = orders.filter(status=status_choice).count()
        
        if DRF_AVAILABLE:
            return Response(stats)
        else:
            return JsonResponse(stats)
    
    # Return order list
    orders_data = []
    for order in orders[:50]:  # Limit to 50 for performance
        if DRF_AVAILABLE:
            order_data = OrderSerializer(order).data
        else:
            order_data = {
                'id': order.id,
                'order_id': str(order.order_id),
                'customer_name': order.customer_name,
                'customer_email': order.customer_email,
                'status': order.status,
                'total_amount': float(order.total_amount),
                'created_at': order.created_at.isoformat()
            }
        
        order_data['customer_name'] = order.user.get_full_name() or order.user.username if order.user else 'Guest'
        order_data['customer_email'] = order.user.email if order.user else ''
        order_data['items_count'] = order.orderitem_set.count()
        orders_data.append(order_data)
    
    if DRF_AVAILABLE:
        return Response(orders_data)
    else:
        return JsonResponse(orders_data, safe=False)


@api_view(['POST']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def mark_message_read_api(request, message_id):
    """API endpoint to mark contact message as read"""
    try:
        message = get_object_or_404(ContactMessage, id=message_id)
        message.is_read = True
        message.save()
        
        response_data = {
            'success': True,
            'message': 'Message marked as read'
        }
        
        if DRF_AVAILABLE:
            return Response(response_data)
        else:
            return JsonResponse(response_data)
            
    except Exception as e:
        error_data = {
            'success': False,
            'error': str(e)
        }
        
        if DRF_AVAILABLE:
            return Response(error_data, status=400)
        else:
            return JsonResponse(error_data, status=400)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_customers_api(request):
    """Customers API endpoint"""
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')
    
    # Apply search filter
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Get customer stats
    if request.path.endswith('/stats/'):
        today = timezone.now().date()
        stats = {
            'total': customers.count(),
            'active_this_month': customers.filter(
                last_login__gte=today - timedelta(days=30)
            ).count(),
            'new_this_week': customers.filter(
                date_joined__gte=today - timedelta(days=7)
            ).count(),
            'vip_customers': customers.annotate(
                order_count=Count('order')
            ).filter(order_count__gte=10).count()
        }
        
        if DRF_AVAILABLE:
            return Response(stats)
        else:
            return JsonResponse(stats)
    
    # Add order statistics to each customer
    customers_data = []
    for customer in customers[:50]:  # Limit for performance
        customer_orders = Order.objects.filter(user=customer)
        
        if DRF_AVAILABLE:
            customer_data = UserSerializer(customer).data
        else:
            customer_data = {
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'date_joined': customer.date_joined.isoformat(),
                'is_active': customer.is_active
            }
            
        customer_data['total_orders'] = customer_orders.count()
        customer_data['total_spent'] = customer_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        customer_data['last_order_date'] = customer_orders.order_by('-created_at').first().created_at if customer_orders.exists() else None
        customers_data.append(customer_data)
    
    if DRF_AVAILABLE:
        return Response(customers_data)
    else:
        return JsonResponse(customers_data, safe=False)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_reports_api(request):
    """Reports API endpoint"""
    report_type = request.GET.get('type', 'sales')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Default date range
    if not date_from:
        date_from = (timezone.now().date() - timedelta(days=7)).isoformat()
    if not date_to:
        date_to = timezone.now().date().isoformat()
    
    response_data = {
        'metrics': {
            'total_revenue': 0,
            'total_orders': 0,
            'avg_order_value': 0,
            'new_customers': 0,
            'revenue_change': 0,
            'orders_change': 0,
            'aov_change': 0,
            'customers_change': 0
        },
        'chart_data': [],
        'secondary_chart': [],
        'table_data': []
    }
    
    # Get orders in date range
    orders = Order.objects.filter(
        created_at__date__gte=date_from,
        created_at__date__lte=date_to
    )
    
    if report_type == 'sales':
        # Sales report data
        response_data['metrics']['total_revenue'] = orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        response_data['metrics']['total_orders'] = orders.count()
        
        if orders.exists():
            response_data['metrics']['avg_order_value'] = response_data['metrics']['total_revenue'] / orders.count()
        
        # Daily sales data for chart
        from django.db.models.functions import TruncDate
        daily_sales = orders.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('total_amount'),
            count=Count('id')
        ).order_by('date')
        
        response_data['chart_data'] = [
            {
                'date': item['date'].isoformat(),
                'value': float(item['revenue'] or 0),
                'revenue': float(item['revenue'] or 0),
                'orders': item['count']
            }
            for item in daily_sales
        ]
        
        response_data['table_data'] = [
            {
                'date': item['date'].isoformat(),
                'orders': item['count'],
                'revenue': float(item['revenue'] or 0),
                'avg_order_value': float(item['revenue'] / item['count']) if item['count'] > 0 else 0
            }
            for item in daily_sales
        ]
    
    # Category stats for secondary chart
    category_stats = OrderItem.objects.filter(
        order__in=orders
    ).values('menu_item__category').annotate(
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_revenue')[:5]
    
    response_data['secondary_chart'] = [
        {
            'label': dict(MenuItem.CATEGORY_CHOICES).get(item['menu_item__category'], 'No Category'),
            'value': float(item['total_revenue'] or 0)
        }
        for item in category_stats
    ]
    
    if DRF_AVAILABLE:
        return Response(response_data)
    else:
        return JsonResponse(response_data)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_categories_api(request):
    """Categories API endpoint"""
    categories = Category.objects.all().order_by('name')
    categories_data = []
    for category in categories:
        if DRF_AVAILABLE:
            category_data = CategorySerializer(category).data
        else:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'image_url': category.image_url,
                'is_active': category.is_active,
                'created_at': category.created_at.isoformat()
            }
        category_data['items_count'] = MenuItem.objects.filter(category_obj=category).count()
        categories_data.append(category_data)
    
    if DRF_AVAILABLE:
        return Response(categories_data)
    else:
        return JsonResponse(categories_data, safe=False)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_order_detail_api(request, order_id):
    """Single order detail API endpoint"""
    try:
        order = Order.objects.select_related('user').prefetch_related(
            'orderitem_set__menu_item'
        ).get(id=order_id)
        
        if DRF_AVAILABLE:
            order_data = OrderSerializer(order).data
        else:
            order_data = {
                'id': order.id,
                'order_id': str(order.order_id),
                'customer_name': order.customer_name,
                'customer_email': order.customer_email,
                'status': order.status,
                'total_amount': float(order.total_amount),
                'created_at': order.created_at.isoformat(),
                'notes': order.notes
            }
            
        order_data['customer_name'] = order.user.get_full_name() or order.user.username if order.user else 'Guest'
        order_data['customer_email'] = order.user.email if order.user else ''
        order_data['customer_phone'] = getattr(order.user.userprofile, 'phone', '') if order.user and hasattr(order.user, 'userprofile') else ''
        
        # Add order items details
        items_data = []
        for item in order.orderitem_set.all():
            items_data.append({
                'menu_item_name': item.menu_item.name,
                'price': float(item.price),
                'quantity': item.quantity,
                'subtotal': float(item.price * item.quantity)
            })
        order_data['items'] = items_data
        
        if DRF_AVAILABLE:
            return Response(order_data)
        else:
            return JsonResponse(order_data)
    except Order.DoesNotExist:
        error_response = {'error': 'Order not found'}
        if DRF_AVAILABLE:
            return Response(error_response, status=404)
        else:
            return JsonResponse(error_response, status=404)


@api_view(['GET']) if DRF_AVAILABLE else lambda f: f
@permission_classes([IsAdminUser]) if DRF_AVAILABLE else lambda f: f
def admin_customer_detail_api(request, customer_id):
    """Single customer detail API endpoint"""
    try:
        customer = User.objects.get(id=customer_id, is_staff=False)
        
        if DRF_AVAILABLE:
            customer_data = UserSerializer(customer).data
        else:
            customer_data = {
                'id': customer.id,
                'username': customer.username,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'date_joined': customer.date_joined.isoformat(),
                'is_active': customer.is_active
            }
        
        # Add customer statistics
        customer_orders = Order.objects.filter(user=customer)
        customer_data['total_orders'] = customer_orders.count()
        customer_data['total_spent'] = customer_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        customer_data['last_order_date'] = customer_orders.order_by('-created_at').first().created_at if customer_orders.exists() else None
        
        # Add recent orders
        recent_orders = customer_orders.order_by('-created_at')[:5]
        if DRF_AVAILABLE:
            customer_data['recent_orders'] = OrderSerializer(recent_orders, many=True).data
        else:
            customer_data['recent_orders'] = [{
                'id': order.id,
                'order_id': str(order.order_id),
                'total_amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat()
            } for order in recent_orders]
        
        if DRF_AVAILABLE:
            return Response(customer_data)
        else:
            return JsonResponse(customer_data)
    except User.DoesNotExist:
        error_response = {'error': 'Customer not found'}
        if DRF_AVAILABLE:
            return Response(error_response, status=404)
        else:
            return JsonResponse(error_response, status=404)


# ============================================================================
# ADVANCED INVENTORY MANAGEMENT
# ============================================================================

@staff_member_required
def admin_inventory(request):
    """Inventory management view"""
    context = {
        'page_title': 'Inventory Management',
        'low_stock_items': MenuItem.objects.filter(stock__lte=5, is_available=True),
        'out_of_stock_items': MenuItem.objects.filter(stock=0, is_available=True),
        'total_items': MenuItem.objects.filter(is_available=True).count(),
    }
    return render(request, 'admin_dashboard/inventory.html', context)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def inventory_alerts_api(request):
    """API endpoint for inventory alerts"""
    low_stock_threshold = int(request.GET.get('threshold', 5))
    
    low_stock_items = MenuItem.objects.filter(
        stock__lte=low_stock_threshold,
        stock__gt=0,
        is_available=True
    ).values('id', 'name', 'stock', 'category')
    
    out_of_stock_items = MenuItem.objects.filter(
        stock=0,
        is_available=True
    ).values('id', 'name', 'category')
    
    return Response({
        'low_stock_items': list(low_stock_items),
        'out_of_stock_items': list(out_of_stock_items),
        'alerts_count': len(low_stock_items) + len(out_of_stock_items)
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_stock_update(request):
    """Bulk update stock levels"""
    try:
        updates = request.data.get('updates', [])
        
        for update in updates:
            item_id = update.get('id')
            new_stock = update.get('stock')
            
            if item_id and new_stock is not None:
                MenuItem.objects.filter(id=item_id).update(stock=new_stock)
        
        return Response({
            'success': True,
            'message': f'Updated stock for {len(updates)} items',
            'updated_count': len(updates)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)