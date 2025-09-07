@echo off
echo ============================================
echo  Django Coffee Shop - Fast Setup Script
echo ============================================
echo.

cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

echo [1/4] Running migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo [2/4] Populating menu with new data...
python manage.py populate_menu
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Menu population failed!
    pause
    exit /b 1
)

echo [3/4] Collecting static files...
python manage.py collectstatic --noinput
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Static files collection had issues, continuing...
)

echo [4/4] Starting Django server...
echo.
echo ================================================
echo   🚀 Coffee Shop Server Starting...
echo   📱 Open: http://127.0.0.1:8000/
echo   📋 Menu: http://127.0.0.1:8000/menu/
echo   🔌 API:  http://127.0.0.1:8000/api/menu/
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 127.0.0.1:8000