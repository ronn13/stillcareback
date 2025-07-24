# Care Backend - Django Application

A comprehensive Django backend for a care management system with REST API endpoints for appointment management, client tracking, and visit monitoring.

## Features

- **User Authentication**: Custom user model with multi-method login (username/password, 6-digit code, biometric)
- **Client Management**: Full CRUD operations for client records
- **Appointment Management**: Scheduling, tracking, and visit management
- **Visit Monitoring**: Real-time location tracking and visit status updates
- **Seizure Tracking**: Comprehensive seizure recording and monitoring
- **Notes System**: Document and image uploads for visit notes
- **REST API**: Complete API for mobile app integration
- **Admin Interface**: Django admin for data management

## Technology Stack

- **Backend**: Django 5.2.4
- **API**: Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: Custom user model with token authentication
- **File Storage**: Local storage with media file handling
- **CORS**: Cross-origin resource sharing support

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd care_backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv careenv
   source careenv/bin/activate  # On Windows: careenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your local settings
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000
   - Admin interface: http://localhost:8000/admin
   - API documentation: http://localhost:8000/appointments/api-auth/

## Railway.app Deployment

### Prerequisites

- Railway.app account
- Git repository with your code

### Deployment Steps

1. **Connect to Railway.app**
   - Go to [Railway.app](https://railway.app)
   - Sign in with your GitHub account
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure Environment Variables**
   In Railway.app dashboard, add these environment variables:
   ```
   SECRET_KEY=your-secure-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1,your-railway-domain.railway.app
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://your-frontend-domain.com
   ```

3. **Add PostgreSQL Database**
   - In Railway.app dashboard, click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Deploy**
   - Railway will automatically detect the Django project
   - It will run the build process using the `Procfile`
   - The application will be deployed and accessible via the provided URL

### Railway.app Configuration Files

- **Procfile**: Specifies how to run the application
- **requirements.txt**: Lists Python dependencies
- **runtime.txt**: Specifies Python version
- **railway.json**: Railway.app specific configuration
- **build.sh**: Custom build script (optional)

### Post-Deployment Setup

1. **Run migrations**
   ```bash
   # In Railway.app shell or via CLI
   python manage.py migrate
   ```

2. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## API Documentation

The complete API documentation is available in `CARE_APP_API_DOCUMENTATION.md` and includes:

- Authentication endpoints
- Client management
- Appointment management
- Visit tracking
- Seizure recording
- Notes management
- Location logging

### Key API Endpoints

- **Authentication**: `/api/auth/`
- **Appointments**: `/appointments/api/staff/appointments/`
- **Seizures**: `/appointments/api/staff/seizures/`
- **Notes**: `/api/notes/`
- **Clients**: `/api/clients/`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generated automatically |
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed host domains | localhost,127.0.0.1 |
| `DATABASE_URL` | Database connection string | SQLite (local) |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | localhost:3000 |
| `RAILWAY_STATIC_URL` | Railway static URL | None |

## Database Schema

The application includes the following main models:

- **CustomUser**: Extended user model with staff roles
- **Client**: Client information and care details
- **Appointment**: Scheduled appointments and visits
- **Seizure**: Seizure tracking and monitoring
- **Note**: Visit notes with file attachments
- **VisitLocationLog**: Location tracking during visits
- **InvoiceGroup**: Billing and invoicing

## Security Features

- Custom user authentication
- Token-based API authentication
- CORS protection
- CSRF protection
- Secure headers (production)
- Input validation and sanitization

## Monitoring and Logging

- Django admin interface for data management
- REST API for mobile app integration
- Comprehensive error handling
- Human-readable error messages

## Support

For issues and questions:
1. Check the API documentation
2. Review the Django admin interface
3. Check Railway.app logs for deployment issues
4. Ensure all environment variables are set correctly

## License

This project is proprietary software for care management systems.