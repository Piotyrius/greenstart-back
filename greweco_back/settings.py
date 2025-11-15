"""
Django settings for greweco_back project.
"""
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'apps.core',
    'apps.authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'greweco_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'greweco_back.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Check if using Cloud SQL
USE_CLOUD_SQL = env.bool('USE_CLOUD_SQL', default=False)

if USE_CLOUD_SQL:
    # Cloud SQL configuration
    CLOUD_SQL_CONNECTION_NAME = env('CLOUD_SQL_CONNECTION_NAME', default='')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME', default='greweco_db'),
            'USER': env('DATABASE_USER', default='postgres'),
            'PASSWORD': env('DATABASE_PASSWORD', default=''),
            'HOST': f'/cloudsql/{CLOUD_SQL_CONNECTION_NAME}',
            'PORT': '',
        }
    }
else:
    # Local database configuration
    # Use SQLite for easier local development (no PostgreSQL setup needed)
    # Or use PostgreSQL if DATABASE_HOST is set
    DATABASE_HOST = env('DATABASE_HOST', default='')
    
    if DATABASE_HOST:
        # Local PostgreSQL configuration
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': env('DATABASE_NAME', default='greweco_db'),
                'USER': env('DATABASE_USER', default='postgres'),
                'PASSWORD': env('DATABASE_PASSWORD', default='postgres'),
                'HOST': DATABASE_HOST,
                'PORT': env('DATABASE_PORT', default='5432'),
            }
        }
    else:
        # SQLite for local development (no setup needed)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=['http://localhost:3000', 'http://127.0.0.1:3000']
)

CORS_ALLOW_CREDENTIALS = True

# Google Cloud Storage Settings
GS_BUCKET_NAME = env('GS_BUCKET_NAME', default='greweco-certificates')
GOOGLE_CLOUD_PROJECT_ID = env('GOOGLE_CLOUD_PROJECT_ID', default='')
# For local development, use service account key file
# For Cloud Run, leave empty - uses default service account
GOOGLE_APPLICATION_CREDENTIALS = env('GOOGLE_APPLICATION_CREDENTIALS', default='')
# Note: Install django-storages[google] for GoogleCloudStorage backend
# For now, we'll handle GCS uploads directly in pdf_generator.py
# DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# GS_DEFAULT_ACL = 'publicRead'

# Google Maps API Key (for future use)
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY', default='')

# Cloud Scheduler Secret (for securing HTTP triggers)
CLOUD_SCHEDULER_SECRET = env('CLOUD_SCHEDULER_SECRET', default='')

# Port for Cloud Run (default: 8080)
PORT = env.int('PORT', default=8080)

# Security settings for production (Cloud Run)
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

