# Set up Django environment
$env:DJANGO_SETTINGS_MODULE = "coffeeshop.settings"

# Run Python script to check categories
python -c "
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')
django.setup()

from coffee.models import Category

# Check categories
print('Categories count:', Category.objects.count())
categories = list(Category.objects.values('id', 'name'))
print('Categories:', categories)
"