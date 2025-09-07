from django.core.management.base import BaseCommand
from coffee.models import Category

class Command(BaseCommand):
    help = 'Create sample categories for the coffee shop'

    def handle(self, *args, **options):
        # Sample categories data
        categories_data = [
            {'name': 'Coffee', 'description': 'Hot and cold coffee beverages'},
            {'name': 'Espresso', 'description': 'Espresso-based drinks'},
            {'name': 'Cold Drinks', 'description': 'Refreshing cold beverages'},
            {'name': 'Pastries', 'description': 'Freshly baked pastries'},
            {'name': 'Sandwiches', 'description': 'Delicious sandwiches'},
            {'name': 'Desserts', 'description': 'Sweet treats and desserts'}
        ]
        
        # Create categories
        created_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    f'Category already exists: {category.name}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} categories')
        )