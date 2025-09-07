#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')
django.setup()

# Quick server start script
def main():
    print("🚀 Starting Django Coffee Shop Server...")
    
    try:
        # Quick checks
        from django.core.management import call_command
        print("✅ Django setup complete")
        
        # Create superuser if needed
        from django.contrib.auth.models import User
        if not User.objects.filter(username='aayushi2001').exists():
            print("👤 Creating superuser...")
            call_command('setup_superuser')
        
        print("🌐 Server starting at http://127.0.0.1:8000/")
        print("🔐 Admin Dashboard: http://127.0.0.1:8000/dashboard/")
        print("📋 Django Admin: http://127.0.0.1:8000/admin/")
        print("\n💳 Admin Login:")
        print("   Username: aayushi2001")
        print("   Password: Aayu$2001")
        print("\n" + "="*50)
        
        # Start server
        execute_from_command_line(['manage.py', 'runserver'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Trying alternative startup...")
        
        # Alternative startup
        os.system('python manage.py migrate --run-syncdb')
        os.system('python manage.py runserver')

if __name__ == '__main__':
    main()