@echo off
echo Starting Django Coffee Shop Server...
echo =====================================

cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

echo Current directory: %CD%
echo.

echo Checking if manage.py exists...
if exist manage.py (
    echo ✓ manage.py found
) else (
    echo ✗ manage.py not found - Please check directory
    pause
    exit /b
)

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo Starting Django development server...
echo Open your browser and go to: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 127.0.0.1:8000

pause