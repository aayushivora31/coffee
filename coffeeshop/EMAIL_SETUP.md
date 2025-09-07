# CoffeeShop Email Notification System

## Overview
This Django Coffee Shop project includes a comprehensive email notification system that automatically sends emails to `aayushivora31@gmail.com` for:

1. **New User Signups** - When someone creates an account
2. **New Orders** - When customers place orders
3. **Contact Form Submissions** - When users submit the contact form
4. **API Form Submissions** - When forms are submitted via API
5. **Menu Item Additions** - When new menu items are added (optional)

## Configuration

### 1. Gmail SMTP Setup

#### settings.py Configuration
```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-app-password')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Email notification settings
NOTIFICATION_EMAIL = 'aayushivora31@gmail.com'
EMAIL_TIMEOUT = 60
```

#### Environment Variables (.env file)
```bash
EMAIL_HOST_USER=your-gmail-address@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

### 2. Gmail App Password Setup

**Important**: You MUST use an App Password, not your regular Gmail password.

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (must be enabled first)
3. App passwords → Generate app password for "Mail"
4. Use the generated 16-character password in your `.env` file

### 3. Environment File Setup

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Update `.env` with your actual Gmail credentials:
   ```bash
   EMAIL_HOST_USER=youremail@gmail.com
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   ```

## Email Templates

All email templates are located in: `coffee/templates/coffee/emails/`

### Available Templates:
- `user_signup.html` - New user registration notification
- `order_created.html` - New order notification with items and totals
- `contact_form.html` - Contact form submission notification
- `generic_form.html` - Generic form submission notification
- `menu_item_added.html` - New menu item notification

### Template Features:
- ✅ Professional HTML design with inline CSS
- ✅ Coffee shop branding and styling
- ✅ Responsive design for mobile devices
- ✅ Currency symbol display (₹, £, €)
- ✅ Order item details with pricing
- ✅ User information and timestamps
- ✅ Fallback plain text versions

## Django Signals

The email system uses Django signals for automatic email sending:

### signals.py Features:
- `user_signup_notification` - Triggered on User creation
- `order_creation_notification` - Triggered on Order creation
- `contact_form_notification` - Triggered on ContactMessage creation
- `menu_item_notification` - Triggered on MenuItem creation (optional)
- `send_custom_form_notification` - Manual trigger for any form

### Signal Registration:
Signals are automatically registered in `apps.py`:

```python
class CoffeeConfig(AppConfig):
    def ready(self):
        import coffee.signals
```

## Testing the Email System

### 1. Management Command Testing
```bash
# Test basic email sending
python manage.py test_email --type=test

# Test user signup email template
python manage.py test_email --type=signup

# Test order creation email template
python manage.py test_email --type=order

# Test contact form email template
python manage.py test_email --type=contact
```

### 2. Live Testing
1. **User Signup**: Create a new account on `/signup/`
2. **Contact Form**: Submit the contact form on `/contact/`
3. **Place Order**: Add items to cart and complete checkout
4. **Admin Panel**: Add new menu items via Django admin

### 3. Debug Email Issues
```bash
# Check Django logs for email errors
tail -f django.log

# Test SMTP connection
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@email.com', ['to@email.com'])
```

## Email Content Examples

### User Signup Email
- Subject: "New User Registration - username"
- Contains: Username, email, name, registration date
- Template: Professional welcome notification

### Order Creation Email  
- Subject: "New Order Created - Order #12345"
- Contains: Customer info, order items, quantities, prices, total
- Template: Detailed order breakdown with currency symbols

### Contact Form Email
- Subject: "New Contact Form Submission - Name"
- Contains: Sender name, email, message, timestamp
- Template: Professional inquiry notification with reply-to link

## Error Handling

### Automatic Error Handling:
- All email functions use `fail_silently=False` for debugging
- Logging captures email send success/failure
- Graceful fallback if email service unavailable

### Common Issues & Solutions:

1. **"Authentication failed" Error**
   - Solution: Use App Password, not regular password
   - Enable 2-Factor Authentication on Gmail

2. **"SMTPRecipientsRefused" Error**
   - Solution: Check recipient email address
   - Verify Gmail account allows external SMTP

3. **"Connection timed out" Error**
   - Solution: Check firewall settings
   - Verify EMAIL_PORT and EMAIL_USE_TLS settings

4. **Email not received**
   - Check spam/junk folder
   - Verify NOTIFICATION_EMAIL setting
   - Test with different recipient email

## Security Best Practices

### Implemented Security:
- ✅ Environment variables for sensitive data
- ✅ App passwords instead of main account password
- ✅ TLS encryption for email transmission
- ✅ Input validation on all forms
- ✅ CSRF protection on form submissions

### Production Recommendations:
- Use dedicated email service (SendGrid, Mailgun)
- Implement email rate limiting
- Add email delivery confirmation
- Monitor email bounce rates
- Set up proper SPF/DKIM records

## Customization

### Changing Notification Email:
Update `settings.py`:
```python
NOTIFICATION_EMAIL = 'your-new-email@domain.com'
```

### Adding New Email Types:
1. Create new signal in `signals.py`
2. Create new email template in `emails/` folder
3. Register signal trigger in appropriate view/model

### Customizing Email Templates:
1. Edit HTML templates in `coffee/templates/coffee/emails/`
2. Maintain responsive design and inline CSS
3. Test across different email clients

## Integration with Existing Code

### The email system integrates with:
- ✅ Django User model (signup notifications)
- ✅ ContactMessage model (form submissions)
- ✅ Order model (order notifications)
- ✅ MenuItem model (menu updates)
- ✅ All Django views and forms
- ✅ AJAX form submissions
- ✅ Multi-currency support
- ✅ Authentication system

### No Breaking Changes:
- All existing functionality preserved
- Email notifications are additional feature
- Graceful fallback if email fails
- No database schema changes required

## Monitoring & Maintenance

### Log Monitoring:
```python
# Check email logs
import logging
logger = logging.getLogger(__name__)
# Email success/failure logged automatically
```

### Performance Considerations:
- Emails sent asynchronously via signals
- No blocking of user experience
- Consider Celery for high-volume production use

### Regular Maintenance:
- Monitor email delivery rates
- Update email templates seasonally
- Review and archive old notifications
- Test email system after Django updates

## Ready for Production

This email notification system is production-ready with:
- ✅ Professional email templates
- ✅ Secure SMTP configuration
- ✅ Comprehensive error handling
- ✅ Testing commands included
- ✅ Documentation provided
- ✅ Security best practices
- ✅ Multi-currency support
- ✅ Responsive design
- ✅ Django signals integration