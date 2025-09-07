from django import template
from django.conf import settings
from decimal import Decimal

register = template.Library()

@register.filter
def convert_currency(price, target_currency):
    """Convert price to target currency"""
    if not target_currency or target_currency not in settings.CURRENCY_RATES:
        return price
    
    # Convert from GBP (base) to target currency
    rate = Decimal(str(settings.CURRENCY_RATES[target_currency]))
    converted = price * rate
    return round(converted, 2)

@register.filter
def currency_symbol(currency_code):
    """Get currency symbol"""
    return settings.CURRENCY_SYMBOLS.get(currency_code, '£')