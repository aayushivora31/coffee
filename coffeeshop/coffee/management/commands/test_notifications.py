from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from coffee.signals import send_notification_email
from django.utils import timezone

class Command(BaseCommand):
    help = 'Test email notifications to aayushivora31@gmail.com'

    def handle(self, *args, **options):
        try:
            # Test basic email
            send_mail(
                subject='CoffeeShop Test Email',
                message='This is a test email. If you receive this, the email system is working!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Test email sent successfully to {settings.NOTIFICATION_EMAIL}!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send email: {str(e)}')
            )