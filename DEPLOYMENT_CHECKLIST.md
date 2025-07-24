# Railway.app Deployment Checklist

## Pre-Deployment Checklist

### ✅ Code Preparation
- [ ] All code is committed to Git repository
- [ ] `requirements.txt` is up to date with all dependencies
- [ ] `Procfile` is created and configured
- [ ] `runtime.txt` specifies Python version
- [ ] `railway.json` is configured
- [ ] `.gitignore` excludes sensitive files

### ✅ Environment Variables
- [ ] `SECRET_KEY` - Generate a secure Django secret key
- [ ] `DEBUG=False` - Set to False for production
- [ ] `ALLOWED_HOSTS` - Include your Railway domain
- [ ] `CORS_ALLOWED_ORIGINS` - Set your frontend domains
- [ ] `DATABASE_URL` - Railway will provide this automatically

### ✅ Database Configuration
- [ ] PostgreSQL database is added to Railway project
- [ ] Database migrations are ready
- [ ] No hardcoded database credentials in code

### ✅ Static Files
- [ ] `STATIC_ROOT` is configured in settings
- [ ] `STATICFILES_STORAGE` is set to whitenoise
- [ ] Static files are properly organized

## Deployment Steps

### 1. Connect to Railway.app
1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

### 2. Configure Environment Variables
In Railway.app dashboard, add these variables:
```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-railway-domain.railway.app
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://your-frontend-domain.com
```

### 3. Add PostgreSQL Database
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically set `DATABASE_URL`

### 4. Deploy
1. Railway will automatically detect Django project
2. Build process will run using `Procfile`
3. Application will be deployed

## Post-Deployment Setup

### 1. Run Migrations
```bash
# In Railway.app shell or via CLI
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Test Application
- [ ] Main site loads correctly
- [ ] Admin interface is accessible
- [ ] API endpoints respond properly
- [ ] Database operations work
- [ ] Static files are served

## Troubleshooting

### Common Issues

#### Build Fails
- Check `requirements.txt` for missing dependencies
- Verify Python version in `runtime.txt`
- Check Railway build logs

#### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check if PostgreSQL service is running
- Ensure migrations are applied

#### Static Files Not Loading
- Verify `STATIC_ROOT` configuration
- Check if `collectstatic` was run
- Ensure whitenoise middleware is enabled

#### CORS Issues
- Check `CORS_ALLOWED_ORIGINS` configuration
- Verify frontend domain is included
- Test API endpoints from frontend

#### Environment Variables
- Verify all required variables are set
- Check variable names and values
- Restart application after changes

### Railway.app Commands

```bash
# Access Railway CLI
railway login
railway link

# View logs
railway logs

# Access shell
railway shell

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is secure and unique
- [ ] `ALLOWED_HOSTS` is properly configured
- [ ] CORS settings are restrictive
- [ ] Database credentials are not in code
- [ ] HTTPS is enabled
- [ ] Admin interface is protected

## Monitoring

- [ ] Set up Railway monitoring
- [ ] Configure error logging
- [ ] Monitor database performance
- [ ] Track API usage
- [ ] Set up alerts for downtime

## Backup Strategy

- [ ] Database backups are configured
- [ ] Static files are backed up
- [ ] Environment variables are documented
- [ ] Deployment process is documented

## Performance Optimization

- [ ] Static files are compressed
- [ ] Database queries are optimized
- [ ] Caching is configured (if needed)
- [ ] CDN is set up (if needed)

## Final Verification

- [ ] All API endpoints work
- [ ] Authentication works
- [ ] File uploads work
- [ ] Database operations work
- [ ] Admin interface is functional
- [ ] Mobile app can connect
- [ ] Error handling works
- [ ] Logs are accessible

## Support Resources

- [Railway.app Documentation](https://docs.railway.app/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) 