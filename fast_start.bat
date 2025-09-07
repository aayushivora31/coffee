@echo off
echo 🚀 Fast Django Coffee Shop Start
cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

echo 📦 Basic migration...
python manage.py migrate --run-syncdb

echo 🌐 Starting server immediately...
echo.
echo 🎉 WEBSITE READY!
echo    🏠 Main Site: http://127.0.0.1:8000/
echo    📋 Django Admin: http://127.0.0.1:8000/admin/
echo.
echo Starting now...
start http://127.0.0.1:8000
python manage.py runserver

pause