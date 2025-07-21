#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def check_and_fix_user():
    print("Checking existing users...")
    users = User.objects.all()
    for user in users:
        print(f"- {user.username} (role: {user.role}, staff: {user.is_staff_member}, active: {user.is_active})")
    
    # Check if test_staff exists
    try:
        user = User.objects.get(username='test_staff')
        print(f"\nUser test_staff exists:")
        print(f"- Role: {user.role}")
        print(f"- Staff member: {user.is_staff_member}")
        print(f"- Active: {user.is_active}")
        print(f"- Password set: {user.has_usable_password()}")
        
        # Fix the user if needed
        if not user.is_staff_member:
            user.is_staff_member = True
            print("Setting is_staff_member to True")
        
        if not user.is_active:
            user.is_active = True
            print("Setting is_active to True")
        
        if not user.has_usable_password():
            user.set_password('testpass123')
            print("Setting password to 'testpass123'")
        
        user.save()
        print("User updated successfully!")
        
        # Create token if it doesn't exist
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"Created new token: {token.key}")
        else:
            print(f"Existing token: {token.key}")
            
    except User.DoesNotExist:
        print("\nUser test_staff does not exist. Creating...")
        user = User.objects.create_user(
            username='test_staff',
            password='testpass123',
            first_name='Test',
            last_name='Staff',
            email='test@example.com',
            role='nurse',
            is_staff_member=True,
            is_active=True
        )
        print(f"Created user: {user.username}")
        
        # Create token
        token = Token.objects.create(user=user)
        print(f"Created token: {token.key}")
    
    print("\nTest credentials:")
    print("Username: test_staff")
    print("Password: testpass123")
    print("Role: Nurse")
    print("Staff Member: Yes")

if __name__ == '__main__':
    check_and_fix_user() 