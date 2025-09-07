# Create sample categories if they don't exist
python -c "
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')
django.setup()

from coffee.models import Category

# Check if categories exist, if not create some sample ones
if Category.objects.count() == 0:
    categories_data = [
        {'name': 'Coffee', 'description': 'Hot and cold coffee beverages'},
        {'name': 'Espresso', 'description': 'Espresso-based drinks'},
        {'name': 'Cold Drinks', 'description': 'Refreshing cold beverages'},
        {'name': 'Pastries', 'description': 'Freshly baked pastries'},
        {'name': 'Sandwiches', 'description': 'Delicious sandwiches'},
        {'name': 'Desserts', 'description': 'Sweet treats and desserts'}
    ]
    
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        print(f'Created category: {category.name}')
else:
    print('Categories already exist:')
    for category in Category.objects.all():
        print(f'- {category.name}')
"

# Navigate to the correct directory and run the Django command
cd "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"
python manage.py create_categories
