#!/usr/bin/env python
"""
Debug script to test CSRF configuration
Run this to check your current CSRF settings
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
django.setup()

print("=== CSRF Configuration Debug ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"CSRF_TRUSTED_ORIGINS: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'Not set')}")
print(f"CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Not set')}")
print(f"CSRF_COOKIE_SAMESITE: {getattr(settings, 'CSRF_COOKIE_SAMESITE', 'Not set')}")
print(f"SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Not set')}")
print(f"SESSION_COOKIE_SAMESITE: {getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Not set')}")

print("\n=== Environment Variables ===")
print(f"SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
print(f"DEBUG: {os.environ.get('DEBUG', 'Not set')}")
print(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'Not set')}")
print(f"CSRF_TRUSTED_ORIGINS: {os.environ.get('CSRF_TRUSTED_ORIGINS', 'Not set')}")

print("\n=== Recommendations ===")
if not settings.DEBUG:
    print("✓ Running in production mode")
    if not getattr(settings, 'CSRF_TRUSTED_ORIGINS', None):
        print("⚠ CSRF_TRUSTED_ORIGINS not set - this will cause CSRF errors!")
    else:
        print("✓ CSRF_TRUSTED_ORIGINS is configured")
else:
    print("ℹ Running in debug mode - CSRF is more lenient") 