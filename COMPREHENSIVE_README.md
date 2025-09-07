# ☕ Coffee Shop - Premium Coffee Experience

A comprehensive Django-based coffee shop application with advanced e-commerce features, admin dashboard, and modern web technologies.

## 🚀 Features Implemented

### 🛍️ E-Commerce Core Features
- **Product Catalog**: Complete menu with categories (Coffee, Espresso, Cold Drinks, Pastries, Desserts)
- **Shopping Cart**: Full cart functionality with quantity management and session support
- **Order Management**: Complete order processing with status tracking
- **User Authentication**: Registration, login, logout with profile management
- **Multi-Currency Support**: GBP and EUR with automatic conversion
- **Stock Management**: Real-time inventory tracking with low stock alerts

### ⭐ Advanced E-Commerce Features
- **Product Reviews & Ratings**: 5-star rating system with review management
- **Wishlist System**: Save favorite items for later purchase
- **Coupon & Discount System**: Promo codes with percentage/fixed discounts
- **Advanced Search**: Intelligent search with filters and sorting options
- **Image Gallery**: High-quality product images with fallback placeholders

### 📊 Admin Dashboard Features
- **Comprehensive Analytics**: Sales metrics, revenue tracking, customer insights
- **Inventory Management**: Stock alerts, bulk updates, automated reordering suggestions
- **Order Processing**: Real-time order tracking and status management
- **Customer Management**: User profiles, order history, communication tools
- **Advanced Reporting**: Sales forecasting, trend analysis, performance metrics
- **Product Management**: CRUD operations with image upload and category management

### 🌐 Modern Web Technologies
- **Progressive Web App (PWA)**: Installable app with offline capabilities
- **Service Worker**: Caching strategies for optimal performance
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Smooth Animations**: CSS transitions and hover effects
- **Interactive UI**: Dynamic components with JavaScript enhancements

### 📧 Communication Features
- **Email Notifications**: Automated emails for orders, signups, and form submissions
- **Contact Forms**: CSRF-protected forms with email integration
- **Toast Notifications**: Real-time user feedback system

## 🛠️ Technical Stack

### Backend
- **Django 4.x**: Web framework with MVT architecture
- **Python 3.x**: Core programming language
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Django REST Framework**: API endpoints for frontend integration

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **JavaScript ES6+**: Modern JavaScript features
- **Bootstrap Icons**: Comprehensive icon library
- **AOS Library**: Scroll animations
- **Chart.js**: Data visualization for admin dashboard

### PWA Technologies
- **Service Worker**: Offline functionality and caching
- **Web App Manifest**: Native app-like experience
- **Background Sync**: Offline order processing
- **Push Notifications**: Real-time user engagement

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CoffeeShop
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   cd coffeeshop
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py setup_superuser
   ```

5. **Populate sample data**
   ```bash
   python manage.py populate_menu
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

### Alternative Quick Start
Use the automated startup script:
```bash
python quick_start.py
```

## 🔐 Admin Credentials

**Username**: aayushi2001  
**Email**: aayushivora31@gmail.com  
**Password**: Aayu$2001

## 📱 Access Points

- **Main Website**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/

## 🌟 Key Pages & Features

### Customer Pages
- **Home** (`/`): Hero section with featured products
- **Menu** (`/menu/`): Complete product catalog with search and filters
- **Cart** (`/cart/`): Shopping cart with quantity management
- **Wishlist** (`/wishlist/`): Saved favorite items
- **Search** (`/search/`): Advanced search with multiple filters
- **About** (`/about/`): Company information
- **Contact** (`/contact/`): Contact form with email integration

### Admin Dashboard
- **Dashboard** (`/dashboard/`): Analytics overview with charts
- **Products** (`/dashboard/products/`): Product management
- **Orders** (`/dashboard/orders/`): Order processing and tracking
- **Customers** (`/dashboard/customers/`): Customer management
- **Inventory** (`/dashboard/inventory/`): Stock management with alerts
- **Reports** (`/dashboard/reports/`): Advanced analytics and forecasting

### API Endpoints
- **Menu API** (`/api/menu/`): Product catalog endpoints
- **Cart API** (`/api/cart/`): Shopping cart operations
- **Review API** (`/api/reviews/`): Product review system
- **Wishlist API** (`/api/wishlist/`): Wishlist management
- **Admin APIs** (`/api/admin/`): Dashboard data endpoints

## 🎨 Design Features

### UI/UX
- **Coffee-themed Design**: Warm brown color palette with professional aesthetics
- **Responsive Layout**: Mobile-first design with Bootstrap 5
- **Interactive Elements**: Hover effects, smooth transitions, loading states
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation
- **Performance**: Optimized images, lazy loading, efficient caching

### PWA Features
- **Installable**: Can be installed as native app on mobile and desktop
- **Offline Support**: Core functionality works without internet
- **Fast Loading**: Service worker caching for instant page loads
- **App-like Experience**: Full-screen mode, splash screen, app icons

## 🔧 Configuration

### Email Settings
Configure email notifications in `settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Currency Settings
Supported currencies: GBP (£), EUR (€)
Default currency: GBP

### PWA Configuration
- **Manifest**: `/static/manifest.json`
- **Service Worker**: `/static/sw.js`
- **Icons**: SVG-based scalable icons

## 📊 Database Models

### Core Models
- **MenuItem**: Product catalog with categories, pricing, and stock
- **Category**: Product categorization system
- **Cart/CartItem**: Shopping cart functionality
- **Order/OrderItem**: Order processing and tracking
- **UserProfile**: Extended user information

### Enhanced Models
- **Review**: Product reviews with star ratings
- **Wishlist/WishlistItem**: User favorites system
- **Coupon/CouponUsage**: Discount and promotion system
- **ContactMessage**: Customer communication

## 🚀 Performance Features

### Caching Strategy
- **Static Files**: Long-term caching for CSS, JS, images
- **API Responses**: Intelligent caching for frequently accessed data
- **Database Queries**: Optimized queries with select_related and prefetch_related
- **Service Worker**: Advanced caching strategies for PWA

### Optimization
- **Image Optimization**: WebP support with fallbacks
- **Code Splitting**: Modular JavaScript loading
- **Database Indexing**: Optimized database queries
- **CDN Integration**: Bootstrap and icons from CDN

## 🔒 Security Features

### Django Security
- **CSRF Protection**: All forms protected with CSRF tokens
- **XSS Prevention**: Template auto-escaping enabled
- **SQL Injection**: Django ORM prevents SQL injection
- **Secure Headers**: Security middleware configured

### Authentication
- **Password Validation**: Strong password requirements
- **Session Management**: Secure session handling
- **User Permissions**: Role-based access control
- **Admin Protection**: Staff-only access to admin features

## 🧪 Testing Strategy

### Test Coverage
- **Unit Tests**: Model and view testing
- **Integration Tests**: End-to-end functionality testing
- **API Tests**: REST API endpoint validation
- **Frontend Tests**: JavaScript functionality testing

### Quality Assurance
- **Code Review**: Consistent coding standards
- **Error Handling**: Comprehensive error management
- **Performance Testing**: Load testing for scalability
- **Security Auditing**: Regular security assessments

## 📈 Analytics & Reporting

### Dashboard Metrics
- **Sales Analytics**: Revenue tracking, trend analysis
- **Customer Insights**: User behavior, purchase patterns
- **Product Performance**: Best sellers, review analysis
- **Inventory Reports**: Stock levels, turnover rates

### Business Intelligence
- **Sales Forecasting**: Predictive analytics for future sales
- **Customer Segmentation**: High-value, regular, occasional customers
- **Trend Analysis**: Seasonal patterns, growth metrics
- **Performance KPIs**: Conversion rates, average order value

## 🌐 Deployment Ready

### Production Configuration
- **Environment Variables**: Secure configuration management
- **Static Files**: Production-ready static file serving
- **Database**: PostgreSQL configuration ready
- **Security**: Production security settings

### Scalability
- **Modular Architecture**: Easy to extend and maintain
- **API-First Design**: Ready for mobile app integration
- **Microservices Ready**: Loosely coupled components
- **Cloud Deployment**: AWS, Heroku, DigitalOcean compatible

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request with documentation

### Code Standards
- **PEP 8**: Python code styling
- **DRY Principle**: Don't repeat yourself
- **SOLID Principles**: Object-oriented design
- **Documentation**: Comprehensive docstrings and comments

## 📞 Support

For technical support or feature requests:
- **Email**: aayushivora31@gmail.com
- **Documentation**: Built-in API documentation
- **Code Comments**: Extensive inline documentation

## 🏆 Project Highlights

### Innovation
- **Full PWA Implementation**: Complete offline functionality
- **Advanced Search**: Intelligent filtering and sorting
- **Real-time Analytics**: Live dashboard updates
- **Modern UX**: Smooth animations and transitions

### Scalability
- **Modular Design**: Easy to extend and customize
- **API Architecture**: Ready for mobile app development
- **Performance Optimized**: Fast loading and responsive
- **Cloud Ready**: Deployment-ready configuration

### Business Value
- **Complete E-commerce**: Full online store functionality
- **Admin Efficiency**: Comprehensive management tools
- **Customer Experience**: Intuitive and engaging interface
- **Growth Ready**: Scalable architecture for expansion

---

**Built with ❤️ and ☕ by the Coffee Shop Team**

*This application represents a complete, production-ready e-commerce solution with modern web technologies and best practices.*# ☕ Coffee Shop - Premium Coffee Experience

A comprehensive Django-based coffee shop application with advanced e-commerce features, admin dashboard, and modern web technologies.

## 🚀 Features Implemented

### 🛍️ E-Commerce Core Features
- **Product Catalog**: Complete menu with categories (Coffee, Espresso, Cold Drinks, Pastries, Desserts)
- **Shopping Cart**: Full cart functionality with quantity management and session support
- **Order Management**: Complete order processing with status tracking
- **User Authentication**: Registration, login, logout with profile management
- **Multi-Currency Support**: GBP and EUR with automatic conversion
- **Stock Management**: Real-time inventory tracking with low stock alerts

### ⭐ Advanced E-Commerce Features
- **Product Reviews & Ratings**: 5-star rating system with review management
- **Wishlist System**: Save favorite items for later purchase
- **Coupon & Discount System**: Promo codes with percentage/fixed discounts
- **Advanced Search**: Intelligent search with filters and sorting options
- **Image Gallery**: High-quality product images with fallback placeholders

### 📊 Admin Dashboard Features
- **Comprehensive Analytics**: Sales metrics, revenue tracking, customer insights
- **Inventory Management**: Stock alerts, bulk updates, automated reordering suggestions
- **Order Processing**: Real-time order tracking and status management
- **Customer Management**: User profiles, order history, communication tools
- **Advanced Reporting**: Sales forecasting, trend analysis, performance metrics
- **Product Management**: CRUD operations with image upload and category management

### 🌐 Modern Web Technologies
- **Progressive Web App (PWA)**: Installable app with offline capabilities
- **Service Worker**: Caching strategies for optimal performance
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Smooth Animations**: CSS transitions and hover effects
- **Interactive UI**: Dynamic components with JavaScript enhancements

### 📧 Communication Features
- **Email Notifications**: Automated emails for orders, signups, and form submissions
- **Contact Forms**: CSRF-protected forms with email integration
- **Toast Notifications**: Real-time user feedback system

## 🛠️ Technical Stack

### Backend
- **Django 4.x**: Web framework with MVT architecture
- **Python 3.x**: Core programming language
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Django REST Framework**: API endpoints for frontend integration

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **JavaScript ES6+**: Modern JavaScript features
- **Bootstrap Icons**: Comprehensive icon library
- **AOS Library**: Scroll animations
- **Chart.js**: Data visualization for admin dashboard

### PWA Technologies
- **Service Worker**: Offline functionality and caching
- **Web App Manifest**: Native app-like experience
- **Background Sync**: Offline order processing
- **Push Notifications**: Real-time user engagement

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CoffeeShop
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   cd coffeeshop
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py setup_superuser
   ```

5. **Populate sample data**
   ```bash
   python manage.py populate_menu
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

### Alternative Quick Start
Use the automated startup script:
```bash
python quick_start.py
```

## 🔐 Admin Credentials

**Username**: aayushi2001  
**Email**: aayushivora31@gmail.com  
**Password**: Aayu$2001

## 📱 Access Points

- **Main Website**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/

## 🌟 Key Pages & Features

### Customer Pages
- **Home** (`/`): Hero section with featured products
- **Menu** (`/menu/`): Complete product catalog with search and filters
- **Cart** (`/cart/`): Shopping cart with quantity management
- **Wishlist** (`/wishlist/`): Saved favorite items
- **Search** (`/search/`): Advanced search with multiple filters
- **About** (`/about/`): Company information
- **Contact** (`/contact/`): Contact form with email integration

### Admin Dashboard
- **Dashboard** (`/dashboard/`): Analytics overview with charts
- **Products** (`/dashboard/products/`): Product management
- **Orders** (`/dashboard/orders/`): Order processing and tracking
- **Customers** (`/dashboard/customers/`): Customer management
- **Inventory** (`/dashboard/inventory/`): Stock management with alerts
- **Reports** (`/dashboard/reports/`): Advanced analytics and forecasting

### API Endpoints
- **Menu API** (`/api/menu/`): Product catalog endpoints
- **Cart API** (`/api/cart/`): Shopping cart operations
- **Review API** (`/api/reviews/`): Product review system
- **Wishlist API** (`/api/wishlist/`): Wishlist management
- **Admin APIs** (`/api/admin/`): Dashboard data endpoints

## 🎨 Design Features

### UI/UX
- **Coffee-themed Design**: Warm brown color palette with professional aesthetics
- **Responsive Layout**: Mobile-first design with Bootstrap 5
- **Interactive Elements**: Hover effects, smooth transitions, loading states
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation
- **Performance**: Optimized images, lazy loading, efficient caching

### PWA Features
- **Installable**: Can be installed as native app on mobile and desktop
- **Offline Support**: Core functionality works without internet
- **Fast Loading**: Service worker caching for instant page loads
- **App-like Experience**: Full-screen mode, splash screen, app icons

## 🔧 Configuration

### Email Settings
Configure email notifications in `settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Currency Settings
Supported currencies: GBP (£), EUR (€)
Default currency: GBP

### PWA Configuration
- **Manifest**: `/static/manifest.json`
- **Service Worker**: `/static/sw.js`
- **Icons**: SVG-based scalable icons

## 📊 Database Models

### Core Models
- **MenuItem**: Product catalog with categories, pricing, and stock
- **Category**: Product categorization system
- **Cart/CartItem**: Shopping cart functionality
- **Order/OrderItem**: Order processing and tracking
- **UserProfile**: Extended user information

### Enhanced Models
- **Review**: Product reviews with star ratings
- **Wishlist/WishlistItem**: User favorites system
- **Coupon/CouponUsage**: Discount and promotion system
- **ContactMessage**: Customer communication

## 🚀 Performance Features

### Caching Strategy
- **Static Files**: Long-term caching for CSS, JS, images
- **API Responses**: Intelligent caching for frequently accessed data
- **Database Queries**: Optimized queries with select_related and prefetch_related
- **Service Worker**: Advanced caching strategies for PWA

### Optimization
- **Image Optimization**: WebP support with fallbacks
- **Code Splitting**: Modular JavaScript loading
- **Database Indexing**: Optimized database queries
- **CDN Integration**: Bootstrap and icons from CDN

## 🔒 Security Features

### Django Security
- **CSRF Protection**: All forms protected with CSRF tokens
- **XSS Prevention**: Template auto-escaping enabled
- **SQL Injection**: Django ORM prevents SQL injection
- **Secure Headers**: Security middleware configured

### Authentication
- **Password Validation**: Strong password requirements
- **Session Management**: Secure session handling
- **User Permissions**: Role-based access control
- **Admin Protection**: Staff-only access to admin features

## 🧪 Testing Strategy

### Test Coverage
- **Unit Tests**: Model and view testing
- **Integration Tests**: End-to-end functionality testing
- **API Tests**: REST API endpoint validation
- **Frontend Tests**: JavaScript functionality testing

### Quality Assurance
- **Code Review**: Consistent coding standards
- **Error Handling**: Comprehensive error management
- **Performance Testing**: Load testing for scalability
- **Security Auditing**: Regular security assessments

## 📈 Analytics & Reporting

### Dashboard Metrics
- **Sales Analytics**: Revenue tracking, trend analysis
- **Customer Insights**: User behavior, purchase patterns
- **Product Performance**: Best sellers, review analysis
- **Inventory Reports**: Stock levels, turnover rates

### Business Intelligence
- **Sales Forecasting**: Predictive analytics for future sales
- **Customer Segmentation**: High-value, regular, occasional customers
- **Trend Analysis**: Seasonal patterns, growth metrics
- **Performance KPIs**: Conversion rates, average order value

## 🌐 Deployment Ready

### Production Configuration
- **Environment Variables**: Secure configuration management
- **Static Files**: Production-ready static file serving
- **Database**: PostgreSQL configuration ready
- **Security**: Production security settings

### Scalability
- **Modular Architecture**: Easy to extend and maintain
- **API-First Design**: Ready for mobile app integration
- **Microservices Ready**: Loosely coupled components
- **Cloud Deployment**: AWS, Heroku, DigitalOcean compatible

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request with documentation

### Code Standards
- **PEP 8**: Python code styling
- **DRY Principle**: Don't repeat yourself
- **SOLID Principles**: Object-oriented design
- **Documentation**: Comprehensive docstrings and comments

## 📞 Support

For technical support or feature requests:
- **Email**: aayushivora31@gmail.com
- **Documentation**: Built-in API documentation
- **Code Comments**: Extensive inline documentation

## 🏆 Project Highlights

### Innovation
- **Full PWA Implementation**: Complete offline functionality
- **Advanced Search**: Intelligent filtering and sorting
- **Real-time Analytics**: Live dashboard updates
- **Modern UX**: Smooth animations and transitions

### Scalability
- **Modular Design**: Easy to extend and customize
- **API Architecture**: Ready for mobile app development
- **Performance Optimized**: Fast loading and responsive
- **Cloud Ready**: Deployment-ready configuration

### Business Value
- **Complete E-commerce**: Full online store functionality
- **Admin Efficiency**: Comprehensive management tools
- **Customer Experience**: Intuitive and engaging interface
- **Growth Ready**: Scalable architecture for expansion

---

**Built with ❤️ and ☕ by the Coffee Shop Team**

*This application represents a complete, production-ready e-commerce solution with modern web technologies and best practices.*