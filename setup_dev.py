#!/usr/bin/env python
"""
Development setup script for Care Backend.
This script helps set up the development environment and handles common issues.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_django_installation():
    """Check if Django is properly installed"""
    print("\n🔍 Checking Django installation...")
    try:
        import django
        print(f"✅ Django {django.get_version()} is installed")
        return True
    except ImportError:
        print("❌ Django is not installed")
        return False

def check_authentication_app():
    """Check if the authentication app is properly configured"""
    print("\n🔍 Checking authentication app...")
    try:
        from authentication.models import User
        print("✅ Custom User model found: authentication.User")
        return True
    except ImportError as e:
        print(f"❌ Custom User model not found: {e}")
        return False

def setup_local_settings():
    """Create local_settings.py if it doesn't exist"""
    local_settings_path = Path("care_backend/local_settings.py")
    
    if local_settings_path.exists():
        print("✅ local_settings.py already exists")
        return True
    
    print("\n📝 Creating local_settings.py for development...")
    
    local_settings_content = '''"""
Local development settings override.
This file should be used only for local development.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Override settings for local development
DEBUG = True

# Use SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Allow all hosts in development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Disable HTTPS requirements in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Custom user model - with development fallback
try:
    # Try to import the custom user model
    from authentication.models import User
    AUTH_USER_MODEL = 'authentication.User'
    print("✓ Using custom User model: authentication.User")
except ImportError as e:
    print(f"⚠ Warning: Could not import custom User model: {e}")
    print("⚠ Falling back to default Django User model for development")
    AUTH_USER_MODEL = 'auth.User'

# Static files configuration for development
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Disable whitenoise in development for easier debugging
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
'''
    
    try:
        with open(local_settings_path, 'w') as f:
            f.write(local_settings_content)
        print("✅ local_settings.py created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create local_settings.py: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Care Backend Development Setup")
    print("=" * 40)
    
    # Check Django installation
    if not check_django_installation():
        print("\n💡 To install Django, run: pip install -r requirements.txt")
        return False
    
    # Check authentication app
    auth_ok = check_authentication_app()
    
    # Setup local settings
    if not setup_local_settings():
        return False
    
    # Run Django checks
    if not run_command("python manage.py check", "Running Django system checks"):
        return False
    
    # Create migrations if needed
    if auth_ok:
        if not run_command("python manage.py makemigrations", "Creating database migrations"):
            print("⚠ Migration creation failed, but continuing...")
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        print("⚠ Migration failed, but continuing...")
    
    print("\n🎉 Development setup completed!")
    print("\n📋 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the development server: python manage.py runserver")
    print("3. Access the admin interface at: http://localhost:8000/admin")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 