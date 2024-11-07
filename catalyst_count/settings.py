import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)  # Default DEBUG to False, change as needed
)

# Read the .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Secret key and debug settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
RUNNING_IN_DOCKER = os.environ.get('RUNNING_IN_DOCKER', 'False') == 'True'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'celery',

    # Your app
    'companies',  # Correct app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# Update ROOT_URLCONF and WSGI_APPLICATION to the correct project name
ROOT_URLCONF = 'catalyst_count.urls'
WSGI_APPLICATION = 'catalyst_count.wsgi.application'
REDIS_HOST = os.environ.get(
    'REDIS_HOST', 'redis' if RUNNING_IN_DOCKER else 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'catalyst_count_db'),
        'USER': os.getenv('DB_USER', 'catalyst_count_db'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'catalyst_count_db'),
        'HOST': os.environ.get('DB_HOST', 'db' if RUNNING_IN_DOCKER else 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# settings.py
CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'  # Adjust as needed


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SITE_ID = 1

# Allauth configurations
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Define the root directory for uploaded files
# This creates a 'media' folder at the root of your project.
MEDIA_URL = '/media/'  # URL for accessing uploaded files

# Full path to the 'company_data' folder inside 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the broker
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'

FILE_UPLOAD_MAX_MEMORY_SIZE = 1288490188
# Optionally, increase the maximum request size
DATA_UPLOAD_MAX_MEMORY_SIZE = 1288490188
