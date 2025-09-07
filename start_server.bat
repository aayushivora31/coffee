@echo off
echo =============================================
echo 🚀 Django Coffee Shop Server Startup
echo =============================================
echo 📍 Project: CoffeeShop Django Application
echo 🌐 Server URL: http://127.0.0.1:8000/
echo 📄 Menu Page: http://127.0.0.1:8000/menu/
echo =============================================
echo.

echo 🔧 Navigating to project directory...
cd coffeeshop

echo ⚡ Starting Django development server...
echo.
python manage.py runserver

echo.
echo ✅ Server stopped. Press any key to exit...
pause