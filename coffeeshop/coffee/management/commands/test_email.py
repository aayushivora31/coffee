from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from coffee.signals import send_notification_email
from django.utils import timezone


class Command(BaseCommand):
    help = 'Test email notification system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='test',
            help='Type of test email to send (test, signup, order, contact)',
        )

    def handle(self, *args, **options):
        email_type = options['type']
        
        try:
            if email_type == 'test':
                self.test_basic_email()
            elif email_type == 'signup':
                self.test_signup_email()
            elif email_type == 'order':
                self.test_order_email()
            elif email_type == 'contact':
                self.test_contact_email()
            else:
                self.stdout.write(
                    self.style.ERROR(f'Unknown email type: {email_type}')
                )
                return
                
            self.stdout.write(
                self.style.SUCCESS(f'✅ {email_type.title()} email sent successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send {email_type} email: {str(e)}')
            )

    def test_basic_email(self):
        """Test basic email sending"""
        subject = 'CoffeeShop Email Test'
        message = 'This is a test email from your CoffeeShop Django application.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.NOTIFICATION_EMAIL]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

    def test_signup_email(self):
        """Test user signup email template"""
        context = {
            'username': 'test_user',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'date_joined': timezone.now(),
        }
        
        send_notification_email(
            subject='Test User Registration Email',
            template_name='user_signup.html',
            context=context
        )

    def test_order_email(self):
        """Test order creation email template"""
        from coffee.models import MenuItem
        
        # Create mock data for testing
        context = {
            'order': {
                'id': 12345,
            },
            'order_items': [
                {
                    'menu_item': {'name': 'Cappuccino'},
                    'quantity': 2,
                    'price': 150.00
                },
                {
                    'menu_item': {'name': 'Chocolate Croissant'},
                    'quantity': 1,
                    'price': 80.00
                }
            ],
            'total_items': 3,
            'customer': {
                'username': 'test_customer',
                'email': 'customer@example.com'
            },
            'total_price': 380.00,
            'currency': 'INR',
            'order_date': timezone.now(),
            'status': 'pending',
        }
        
        send_notification_email(
            subject='Test Order Creation Email',
            template_name='order_created.html',
            context=context
        )

    def test_contact_email(self):
        """Test contact form email template"""
        context = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'message': 'This is a test contact form message. I would like to know more about your coffee beans.',
            'submitted_at': timezone.now(),
        }
        
        send_notification_email(
            subject='Test Contact Form Email',
            template_name='contact_form.html',
            context=context
        )