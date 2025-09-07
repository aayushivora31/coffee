from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order, ContactMessage, MenuItem
import logging

logger = logging.getLogger(__name__)

def send_notification_email(subject, template_name, context, recipient_email=None):
    """
    Helper function to send notification emails
    """
    try:
        # Use the notification email from settings
        to_email = recipient_email or settings.NOTIFICATION_EMAIL
        
        # Render HTML email template
        html_message = render_to_string(f'coffee/emails/{template_name}', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Email sent successfully: {subject} to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {subject}. Error: {str(e)}")
        return False

@receiver(post_save, sender=User)
def user_signup_notification(sender, instance, created, **kwargs):
    """
    Send email notification when a new user signs up
    """
    if created:
        subject = f"New User Registration - {instance.username}"
        context = {
            'user': instance,
            'username': instance.username,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'date_joined': instance.date_joined,
        }
        
        send_notification_email(
            subject=subject,
            template_name='user_signup.html',
            context=context
        )

@receiver(post_save, sender=Order)
def order_creation_notification(sender, instance, created, **kwargs):
    """
    Send email notification when a new order is created
    """
    if created:
        # Calculate order details
        order_items = instance.orderitem_set.all()
        total_items = sum(item.quantity for item in order_items)
        
        subject = f"New Order Created - Order #{instance.id}"
        context = {
            'order': instance,
            'order_items': order_items,
            'total_items': total_items,
            'customer': instance.user,
            'total_price': instance.total_amount,
            'currency': instance.currency,
            'order_date': instance.created_at,
            'status': instance.status,
        }
        
        send_notification_email(
            subject=subject,
            template_name='order_created.html',
            context=context
        )

@receiver(post_save, sender=ContactMessage)
def contact_form_notification(sender, instance, created, **kwargs):
    """
    Send email notification when a contact form is submitted
    """
    if created:
        subject = f"New Contact Form Submission - {instance.name}"
        context = {
            'contact': instance,
            'name': instance.name,
            'email': instance.email,
            'message': instance.message,
            'submitted_at': instance.created_at,
        }
        
        send_notification_email(
            subject=subject,
            template_name='contact_form.html',
            context=context
        )

def send_custom_form_notification(form_type, form_data):
    """
    Generic function to send email notifications for any form submission
    """
    subject = f"New {form_type} Form Submission"
    context = {
        'form_type': form_type,
        'form_data': form_data,
        'submitted_at': form_data.get('submitted_at'),
    }
    
    send_notification_email(
        subject=subject,
        template_name='generic_form.html',
        context=context
    )

# Additional signals for other models if needed
@receiver(post_save, sender=MenuItem)
def menu_item_notification(sender, instance, created, **kwargs):
    """
    Send email notification when a new menu item is added (optional)
    """
    if created:
        subject = f"New Menu Item Added - {instance.name}"
        context = {
            'menu_item': instance,
            'name': instance.name,
            'category': instance.category,
            'price': instance.price,
            'description': instance.description,
            'added_at': instance.created_at,
        }
        
        send_notification_email(
            subject=subject,
            template_name='menu_item_added.html',
            context=context
        )