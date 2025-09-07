@echo off
title Django Coffee Shop - Quick Setup
color 0A
echo.
echo =====================================
echo    DJANGO COFFEE SHOP - FINAL SETUP
echo =====================================
echo.

cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

echo [1/4] 🔧 Checking Django installation...
python --version
python -c "import django; print('Django version:', django.get_version())"

echo.
echo [2/4] 📦 Running database migrations...
python manage.py makemigrations coffee
python manage.py migrate

echo.
echo [3/4] 👤 Creating superuser (if needed)...
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='aayushi2001').exists():
    User.objects.create_superuser('aayushi2001', 'aayushivora31@gmail.com', 'Aayu$2001')
    print('✅ Superuser created successfully!')
else:
    print('✅ Superuser already exists!')
"

echo.
echo [4/4] 🌐 Starting Django development server...
echo.
echo ======================================
echo       🎉 WEBSITE IS READY! 🎉
echo ======================================
echo.
echo 🏠 Main Website: http://127.0.0.1:8000/
echo 📊 Admin Panel:  http://127.0.0.1:8000/admin/
echo.
echo 🔐 Admin Login Credentials:
echo    Username: aayushi2001
echo    Password: Aayu$2001
echo    Email:    aayushivora31@gmail.com
echo.
echo ======================================
echo Press Ctrl+C to stop the server
echo ======================================
echo.

start http://127.0.0.1:8000
python manage.py runserver

echo.
echo Server stopped. Press any key to exit...
pause > nul