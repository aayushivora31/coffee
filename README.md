# ☕ Django Coffee Shop - Complete Admin Dashboard System

A full-featured Django coffee shop website with comprehensive admin dashboard, e-commerce functionality, and responsive design.

## 🚀 Quick Start

### **1. Instant Setup (Recommended)**
```bash
# Navigate to project directory and run:
COMPLETE_SETUP.bat
```

### **2. Manual Setup**
```bash
cd c:\Users\aayus\Projects\CoffeeShop\coffeeshop
python manage.py makemigrations coffee
python manage.py migrate
python manage.py runserver
```

## 🌐 Access Your Website

- **🏠 Main Website**: http://127.0.0.1:8000/
- **📊 Admin Dashboard**: http://127.0.0.1:8000/dashboard/
- **⚙️ Django Admin**: http://127.0.0.1:8000/admin/

## 🔐 Admin Login Credentials

```
Username: aayushi2001
Email:    aayushivora31@gmail.com
Password: Aayu$2001
```

## 📋 Features Completed

### ✅ **Core Website**
- **Home Page** - Responsive landing page
- **Menu System** - 5 categories with dynamic items
- **Cart & Checkout** - Full e-commerce functionality
- **User Authentication** - Login, signup, logout
- **Contact System** - Contact form with email notifications

### ✅ **Admin Dashboard System**
- **📊 Dashboard Analytics** - Real-time metrics and charts
- **📦 Product Management** - Add, edit, delete menu items with stock tracking
- **📋 Order Management** - View, update order status, customer details
- **👥 Customer Management** - User profiles, statistics, communication
- **📈 Reports & Analytics** - Sales data, charts, export functionality

### ✅ **Technical Features**
- **Stock Management** - Real-time inventory tracking
- **Multi-Currency Support** - GBP, EUR display options
- **Email Notifications** - Automated alerts for orders and forms
- **Responsive Design** - Bootstrap 5 mobile-friendly layout
- **AJAX Integration** - Dynamic cart updates and notifications
- **Search & Filtering** - Advanced product and order filtering

## 🗂️ Project Structure

```
CoffeeShop/
├── coffeeshop/
│   ├── coffee/                          # Main Django app
│   │   ├── templates/
│   │   │   ├── coffee/                  # Public website templates
│   │   │   └── admin_dashboard/         # Admin dashboard templates
│   │   ├── management/commands/         # Custom management commands
│   │   ├── models.py                    # Database models
│   │   ├── views.py                     # Main views
│   │   ├── admin_views.py               # Admin dashboard views
│   │   ├── serializers.py               # API serializers
│   │   └── urls.py                      # URL routing
│   ├── coffeeshop/
│   │   ├── settings.py                  # Django settings
│   │   └── urls.py                      # Project URLs
│   └── manage.py                        # Django management script
├── COMPLETE_SETUP.bat                   # One-click setup script
└── README.md                            # This file
```

## 🛠️ Available Management Commands

```bash
# Create/update admin superuser
python manage.py setup_superuser

# Populate sample menu data
python manage.py populate_menu

# Run database migrations
python manage.py makemigrations coffee
python manage.py migrate
```

## 📱 Admin Dashboard Features

### **📊 Main Dashboard**
- Total orders, customers, revenue statistics
- Real-time charts for sales and category performance
- Recent orders overview
- Low stock alerts

### **📦 Product Management**
- Add new menu items with images
- Update stock quantities
- Edit prices and descriptions
- Category management
- Bulk operations

### **📋 Order Management**
- View all orders with filtering
- Update order status (Pending → Delivered)
- Customer communication
- Order details and history

### **👥 Customer Management**
- Customer profiles and statistics
- Order history per customer
- Communication tools
- Customer analytics

### **📈 Reports & Analytics**
- Sales reports with date filtering
- Revenue analysis charts
- Customer behavior insights
- Product performance metrics

## 🔧 Technical Specifications

- **Framework**: Django 4.2+
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, JavaScript, Chart.js
- **Authentication**: Django built-in auth system
- **File Uploads**: Django media handling
- **Email**: SMTP configuration ready

## 🎨 Design Features

- **Responsive Layout** - Works on all devices
- **Modern UI** - Clean, professional design
- **Coffee Theme** - Warm colors and coffee-inspired styling
- **Interactive Elements** - AJAX-powered updates
- **Navigation** - Intuitive sidebar and top navigation

## 🔒 Security Features

- **CSRF Protection** - All forms protected
- **Admin Authentication** - Secure dashboard access
- **Permission Controls** - Role-based access
- **Input Validation** - Form security measures

## 📧 Email Configuration

The system is configured for Gmail SMTP. To enable email notifications:

1. Update `settings.py` with your Gmail credentials
2. Use App Passwords for Gmail 2FA accounts
3. Set environment variables for security

## 🚀 Deployment Notes

- **Debug Mode**: Currently enabled for development
- **Static Files**: Configured for production
- **Media Files**: Image upload ready
- **Database**: Easy migration to PostgreSQL/MySQL

## 🐛 Troubleshooting

### Common Issues:
1. **Port Already in Use**: Change port with `python manage.py runserver 8001`
2. **Database Errors**: Run `python manage.py migrate`
3. **Static Files**: Run `python manage.py collectstatic`

### Quick Fixes:
```bash
# Reset database
python manage.py flush

# Create fresh migrations
python manage.py makemigrations coffee --empty

# Debug mode
python manage.py shell
```

## 📞 Support

For technical support or questions about the admin dashboard system:
- Check Django logs in the terminal
- Verify admin credentials match exactly
- Ensure all migrations are applied

---

## 🎉 **Your Coffee Shop Website is Ready!**

Run `COMPLETE_SETUP.bat` and start managing your coffee shop business with the powerful admin dashboard system!

**Happy Coding! ☕**