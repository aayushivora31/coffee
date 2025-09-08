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

# CoffeeShop Website

A responsive static website for a coffee shop, converted from Django templates to static HTML for GitHub Pages deployment.

## 🌐 Live Demo

[Your site will be available here after deployment](https://[your-username].github.io/[your-repo-name]/)

## 📋 Features

- Fully responsive design using Bootstrap 5
- Modern coffee shop theme with warm color palette
- Complete website with multiple pages:
  - Home page
  - About page
  - Menu page
  - Services page
  - Contact page
  - Shopping cart
  - Checkout page
- Smooth animations with AOS (Animate On Scroll)
- Interactive elements with JavaScript

## 🚀 Deployment to GitHub Pages

1. Create a new repository on GitHub
2. Push this code to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - CoffeeShop website"
   git branch -M main
   git remote add origin https://github.com/your-username/your-repo-name.git
   git push -u origin main
   ```
3. Go to your repository settings on GitHub
4. Scroll down to the "Pages" section
5. Under "Source", select "Deploy from a branch"
6. Choose "main" branch and "/(root)" folder
7. Click "Save"
8. Your site will be published at `https://[your-username].github.io/[your-repo-name]/`

## 📁 Project Structure

```
.
├── index.html          # Home page
├── about.html          # About page
├── menu.html           # Menu page
├── services.html       # Services page
├── contact.html        # Contact page
├── cart.html           # Shopping cart page
├── checkout.html       # Checkout page
├── css/                # Stylesheets directory
│   ├── style.css       # Main stylesheet
│   └── images.css      # Image-related styles
└── README.md           # This file
```

## 🎨 Design Elements

- Coffee-themed color scheme (browns, tans, and accent colors)
- Responsive grid layout that works on mobile, tablet, and desktop
- Interactive navigation with active page highlighting
- Animated elements that trigger on scroll
- Card-based design for content sections
- Custom-styled buttons and form elements

## ⚠️ Important Notes

- This is a static website with no backend functionality
- Contact forms and shopping cart features are for demonstration only
- All images are loaded from external sources (Pexels)
- The site is designed to be hosted on GitHub Pages with no server requirements

## 📞 Support

For issues with the website, please create an issue in this repository.
