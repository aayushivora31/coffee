from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create or update superuser with specified credentials for admin dashboard'

    def handle(self, *args, **options):
        username = 'aayushi2001'
        email = 'aayushivora31@gmail.com'
        password = 'Aayu$2001'
        
        try:
            # Try to get existing user
            user = User.objects.get(username=username)
            
            # Update existing user
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated superuser "{username}"')
            )
            
        except User.DoesNotExist:
            # Create new superuser
            try:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                user.first_name = 'Aayushi'
                user.last_name = 'Vora'
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser "{username}"')
                )
                
            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating superuser: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Admin Dashboard Credentials:')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write('Access: http://127.0.0.1:8000/admin/')
        self.stdout.write('Dashboard: http://127.0.0.1:8000/dashboard/')