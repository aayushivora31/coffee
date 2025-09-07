#!/usr/bin/env python3
"""
Test script for CoffeeShop email notification system
Run this script to verify email configuration and test different email types
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from coffee.signals import send_notification_email
from django.utils import timezone
import json

def test_email_configuration():
    """Test basic email configuration"""
    print("🔧 Testing email configuration...")
    
    required_settings = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'NOTIFICATION_EMAIL'
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not hasattr(settings, setting) or not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        print(f"❌ Missing settings: {', '.join(missing_settings)}")
        return False
    
    print("✅ Email configuration looks good!")
    return True

def test_basic_email():
    """Test sending a basic email"""
    print("\n📧 Testing basic email sending...")
    
    try:
        send_mail(
            subject='CoffeeShop Email Test - Basic',
            message='This is a test email from your CoffeeShop Django application. If you receive this, your email system is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        print("✅ Basic email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send basic email: {str(e)}")
        return False

def test_template_emails():
    """Test all email templates"""
    print("\n🎨 Testing email templates...")
    
    tests = [
        {
            'name': 'User Signup',
            'template': 'user_signup.html',
            'context': {
                'username': 'test_user_123',
                'email': 'testuser@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'date_joined': timezone.now(),
            }
        },
        {
            'name': 'Order Creation',
            'template': 'order_created.html',
            'context': {
                'order': type('Order', (), {'id': 98765})(),
                'order_items': [
                    type('OrderItem', (), {
                        'menu_item': type('MenuItem', (), {'name': 'Cappuccino'})(),
                        'quantity': 2,
                        'price': 150.00
                    })(),
                    type('OrderItem', (), {
                        'menu_item': type('MenuItem', (), {'name': 'Blueberry Muffin'})(),
                        'quantity': 1,
                        'price': 85.00
                    })(),
                ],
                'total_items': 3,
                'customer': type('User', (), {
                    'username': 'coffee_lover',
                    'email': 'customer@example.com'
                })(),
                'total_price': 385.00,
                'currency': 'INR',
                'order_date': timezone.now(),
                'status': 'pending',
            }
        },
        {
            'name': 'Contact Form',
            'template': 'contact_form.html',
            'context': {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com',
                'message': 'Hello! I love your coffee shop website. I\'m interested in your premium coffee beans and would like to know more about bulk ordering options. Thank you!',
                'submitted_at': timezone.now(),
            }
        }
    ]
    
    success_count = 0
    for test in tests:
        try:
            print(f"  📤 Sending {test['name']} email...")
            send_notification_email(
                subject=f"CoffeeShop Test - {test['name']}",
                template_name=test['template'],
                context=test['context']
            )
            print(f"  ✅ {test['name']} email sent!")
            success_count += 1
        except Exception as e:
            print(f"  ❌ {test['name']} email failed: {str(e)}")
    
    print(f"\n📊 Template Email Results: {success_count}/{len(tests)} successful")
    return success_count == len(tests)

def print_email_info():
    """Print current email configuration info"""
    print("\n📋 Current Email Configuration:")
    print(f"  Host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    print(f"  Port: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
    print(f"  TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
    print(f"  From Email: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    print(f"  Notification Email: {getattr(settings, 'NOTIFICATION_EMAIL', 'Not set')}")
    print(f"  Password Set: {'Yes' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'No'}")

def main():
    """Main test function"""
    print("🚀 CoffeeShop Email System Test")
    print("=" * 50)
    
    # Check configuration
    if not test_email_configuration():
        print("\n❌ Email configuration issues found. Please check your settings.")
        return False
    
    # Print current configuration
    print_email_info()
    
    # Test basic email
    if not test_basic_email():
        print("\n❌ Basic email test failed. Check your SMTP settings.")
        return False
    
    # Test template emails
    template_success = test_template_emails()
    
    print("\n" + "=" * 50)
    if template_success:
        print("🎉 All email tests passed successfully!")
        print(f"📧 Check {settings.NOTIFICATION_EMAIL} for test emails")
        print("\n💡 Next steps:")
        print("  1. Check your email inbox (including spam folder)")
        print("  2. Verify email templates look correct")
        print("  3. Test live notifications by:")
        print("     - Creating a new user account")
        print("     - Submitting the contact form")
        print("     - Placing a test order")
    else:
        print("⚠️  Some email tests failed. Check the errors above.")
    
    return template_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)