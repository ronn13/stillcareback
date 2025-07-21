from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a test user for mobile app authentication'

    def handle(self, *args, **options):
        # Create test user
        username = 'nurse_test'
        email = 'nurse@test.com'
        password = 'testpass123'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='Nurse',
                role='nurse',
                is_staff_member=True,
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user {username}')
            )
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created new token for user {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Token already exists for user {username}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTest User Credentials:')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Token: {token.key}')
        self.stdout.write(f'Role: {user.get_role_display()}')
        self.stdout.write(f'User ID: {user.id}')
        self.stdout.write(f'\nAPI Login URL: http://localhost:8000/api/auth/login/')
        self.stdout.write(f'Dashboard URL: http://localhost:8000/appointments/api/staff/dashboard/') 