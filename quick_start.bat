@echo off
echo 🚀 Quick Start Django Coffee Shop
cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

echo ✅ Checking Django project...
python manage.py check --deploy
if %errorlevel% neq 0 (
    echo ⚠️ Check failed, trying basic check...
    python manage.py check
)

echo 📦 Running migrations...
python manage.py makemigrations
python manage.py migrate

echo 👤 Setting up admin user...
python manage.py setup_superuser

echo 🌐 Starting server...
echo.
echo 🎉 ACCESS YOUR WEBSITE:
echo    🏠 Main Site: http://127.0.0.1:8000/
echo    📊 Admin Dashboard: http://127.0.0.1:8000/dashboard/
echo    ⚙️ Django Admin: http://127.0.0.1:8000/admin/
echo.
echo 🔐 ADMIN LOGIN:
echo    Username: aayushi2001
echo    Password: Aayu$2001
echo.
echo Starting Django server now...
python manage.py runserver

pause