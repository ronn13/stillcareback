# CSRF Verification Failed - Fix Guide

## Problem
You're getting "Forbidden (403) CSRF verification failed. Request aborted." when trying to log into Django admin on Railway.

## Root Causes
1. **Missing CSRF_TRUSTED_ORIGINS** - Django 4.0+ requires this for CSRF protection
2. **SSL/HTTPS configuration issues** - Railway's HTTPS setup
3. **Cookie domain issues** - Session and CSRF cookies not properly configured

## Solutions Applied

### 1. Settings Changes Made
- Added `CSRF_TRUSTED_ORIGINS` configuration
- Disabled `SECURE_SSL_REDIRECT` temporarily
- Added proper cookie settings
- Made CSRF settings configurable via environment variables

### 2. Railway Environment Variables
Set these environment variables in your Railway dashboard:

```
CSRF_TRUSTED_ORIGINS=https://web-production-83ebd.up.railway.app,https://*.up.railway.app
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=web-production-83ebd.up.railway.app,*.up.railway.app
```

### 3. Alternative Quick Fix
If the above doesn't work, temporarily add this to your settings.py:

```python
# Add this at the bottom of settings.py for temporary fix
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://web-production-83ebd.up.railway.app',
        'https://*.up.railway.app',
        'http://web-production-83ebd.up.railway.app',  # HTTP fallback
    ]
    CSRF_COOKIE_SECURE = False  # Temporarily disable
    SESSION_COOKIE_SECURE = False  # Temporarily disable
```

## Testing Steps

1. **Run the debug script locally:**
   ```bash
   python debug_csrf.py
   ```

2. **Deploy to Railway and check:**
   - Visit your admin URL: `https://web-production-83ebd.up.railway.app/admin/`
   - Check Railway logs for any CSRF-related errors

3. **If still failing, try:**
   - Clear browser cookies for the domain
   - Try in incognito/private mode
   - Check if HTTPS is working properly

## Security Notes
- The temporary fixes above reduce security - only use them to get admin working
- Once working, re-enable `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True`
- Make sure `SECURE_SSL_REDIRECT = True` is enabled once HTTPS is confirmed working

## Common Railway Issues
1. **Domain mismatch** - Make sure your Railway app URL matches `CSRF_TRUSTED_ORIGINS`
2. **HTTPS not working** - Railway should provide HTTPS automatically
3. **Environment variables not set** - Check Railway dashboard for proper configuration

## Next Steps
1. Deploy the updated settings
2. Set the environment variables in Railway
3. Test admin login
4. If working, gradually re-enable security settings
5. Remove any temporary security bypasses 