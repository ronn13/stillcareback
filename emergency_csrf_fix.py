#!/usr/bin/env python
"""
Emergency CSRF fix for Railway deployment
This script temporarily disables CSRF for admin login to get you working immediately
WARNING: This reduces security - only use temporarily!
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
django.setup()

print("=== Emergency CSRF Fix ===")
print("This will temporarily disable CSRF for admin login")
print("WARNING: This reduces security - only use temporarily!")

# Add this to your settings.py at the bottom:
emergency_fix = '''
# EMERGENCY CSRF FIX - REMOVE AFTER FIXING THE ISSUE
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-83ebd.up.railway.app',
    'https://*.up.railway.app',
    'http://web-production-83ebd.up.railway.app',
    'http://*.up.railway.app',
    '*',  # Allow all origins (DANGEROUS - only for emergency)
]

# Temporarily disable secure cookies
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Disable SSL redirect
SECURE_SSL_REDIRECT = False
'''

print("\nAdd this to the BOTTOM of your settings.py file:")
print("=" * 50)
print(emergency_fix)
print("=" * 50)

print("\nAfter adding this:")
print("1. Deploy to Railway")
print("2. Test admin login")
print("3. Once working, remove the emergency fix")
print("4. Set proper CSRF_TRUSTED_ORIGINS environment variable")
print("5. Re-enable security settings")

print("\nAlternative: Set this environment variable in Railway:")
print("CSRF_TRUSTED_ORIGINS=https://web-production-83ebd.up.railway.app,https://*.up.railway.app,http://web-production-83ebd.up.railway.app,http://*.up.railway.app") 