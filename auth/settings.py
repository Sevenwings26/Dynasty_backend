"""
Django 4.2.16.
"""

import os
from pathlib import Path
from datetime import timedelta

# get .env variables
import environ
env = environ.Env()
environ.Env.read_env()
# database 

import dj_database_url

# Environment configuration 
ENVIRONMENT = env('ENVIRONMENT', default="development")
ENVIRONMENT = "production"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

# Hosting platforms 
if ENVIRONMENT == "development":
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'dynasty-backend.onrender.com']

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://arcade-dynasty.vercel.app",
    'https://dynasty-backend.onrender.com'
]

# Application definition

INSTALLED_APPS = [
    # "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
   
    # created app
    "users",

    # rest
    'rest_framework',
    'corsheaders',
    'knox',
    'django_rest_passwordreset',
    'drf_yasg',

    # media production
    'cloudinary_storage',
    'cloudinary',

    # # queue task
    # "django_q"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Knox configuration
REST_KNOX = {
    'TOKEN_TTL': timedelta(days=10),
}
 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',  # Knox token authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Ensuring users are authenticated
    ],
}

APPEND_SLASH = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://arcade-dynasty.vercel.app",
    'https://dynasty-backend.onrender.com',
    'https://www.arcade-dynasty.com',
]

CORS_ALLOWED_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS =[
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
]

# # for asynchronous task 
# Q_CLUSTER = {
#     'name': 'DjangoQCluster',
#     'workers': 4,
#     'recycle': 500,
#     'timeout': 60,
#     'retry': 120,
#     'queue_limit': 50,
#     'bulk': 10,
#     'orm': 'default'  # Use ORM as broker
# }

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = [
    'users.auth_backend.EmailAuthBackend',
    "django.contrib.auth.backends.ModelBackend",  # this line fixed my problem
]


ROOT_URLCONF = "auth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "auth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENVIRONMENT == "development":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        'default':dj_database_url.parse(env("DATABASE_URL"))
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR / 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files
MEDIA_URL = '/media/'
# Specify the directory where media files are stored
if ENVIRONMENT == "development":
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUDINARY_URL': env('CLOUDINARY_URL'),
        'CLOUDINARY_CLOUD_NAME' : env('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': env('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET':env('CLOUDINARY_API_SECRET'),
    }



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#the email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# # EMAIL_PORT = 465
# EMAIL_USE_TLS = True
# # EMAIL_USE_SSL = True
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER")
# ACCOUNT_EMAIL_SUBJECT_PREFIX = env("ACCOUNT_EMAIL_SUBJECT_PREFIX")


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL') 
ACCOUNT_EMAIL_SUBJECT_PREFIX = env("ACCOUNT_EMAIL_SUBJECT_PREFIX")

