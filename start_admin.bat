@echo off
cd /d "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"
echo Checking Django project...
python manage.py check
if %errorlevel% neq 0 (
    echo Django check failed!
    pause
    exit /b 1
)

echo Making migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Makemigrations failed!
    pause
    exit /b 1
)

echo Running migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Migrate failed!
    pause
    exit /b 1
)

echo Creating superuser...
python manage.py setup_superuser
if %errorlevel% neq 0 (
    echo Setup superuser failed!
    pause
    exit /b 1
)

echo All checks passed! Starting server...
python manage.py runserver
pause