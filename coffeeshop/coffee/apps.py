from django.apps import AppConfig


class CoffeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coffee'
    
    def ready(self):
        """Import signals when the app is ready"""
        import coffee.signals
