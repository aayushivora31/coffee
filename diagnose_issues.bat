@echo off
echo ===========================================
echo 🔍 Django Coffee Shop Problem Diagnosis
echo ===========================================
echo.

cd coffeeshop

echo ✅ 1. Checking Django setup...
python manage.py check

echo.
echo ✅ 2. Checking database...
python manage.py showmigrations

echo.
echo ✅ 3. Checking menu data...
python -c "
from django.core.management import execute_from_command_line
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')
django.setup()
from coffee.models import MenuItem
print(f'Total menu items: {MenuItem.objects.count()}')
for category in ['coffee', 'espresso', 'cold_drinks', 'pastries', 'desserts']:
    count = MenuItem.objects.filter(category=category).count()
    print(f'{category.title()}: {count} items')
"

echo.
echo ✅ 4. Checking templates...
dir coffee\templates\coffee\*.html

echo.
echo ✅ 5. Checking static files...
dir coffeeshop\static\css\*.css

echo.
echo ✅ 6. Testing basic views...
python manage.py shell -c "
from django.test import Client
client = Client()
response = client.get('/')
print(f'Home page status: {response.status_code}')
response = client.get('/menu/')
print(f'Menu page status: {response.status_code}')
"

echo.
echo ===========================================
echo 🎯 Diagnosis Complete!
echo If all checks passed, your coffee shop should work properly.
echo Run quick_fix.bat to start the server.
echo ===========================================
pause