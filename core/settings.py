"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from decouple import config # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'allauth',
    'allauth.account',  
    'allauth.socialaccount', 
    'allauth.socialaccount.providers.google',  
    'allauth.socialaccount.providers.facebook',  
    # 'django.contrib.contenttypes',
    # 'django.contrib.postgres',
    'rest_framework',
    'user',
    'listing',
    'chat',
    'payments',
    'location',
    'dashboard',
]

# Set the site ID
SITE_ID = 1

MIGRATION_MODULES = {
    'contenttypes': 'django.contrib.contenttypes.migrations',
}


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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # For regular login
    'allauth.account.auth_backends.AuthenticationBackend',  # For social login
)


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 'users': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'users_db.sqlite3',
    # },
    # 'listings': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'listing_db.sqlite3',
    # }
}

# DATABASE_ROUTERS = ['user.router.AuthRouter', 'listing.router.ListingRouter']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Enable email as a required field
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True  # This helps manage redirects correctly
ACCOUNT_LOGOUT_REDIRECTS = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_ADAPTER = 'user.adapters.SocialAccountAdapter'



CAMPAY_USERNAME = config('CAMPAY_USERNAME')
CAMPAY_PASSWORD = config('CAMPAY_PASSWORD')



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
GOOGLE_API_KEY = config('GOOGLE_API_KEY')


# settings.py

# For development
EMAIL_BACKEND = config('EMAIL_BACKEND')

# for production
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('O2AUTH_CLIENT_ID'),
            'secret': config('O2AUTH_CLIENT_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_FORMS = {
    'signup': 'user.forms.UserForm',
    }


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

O2AUTH_CLIENT_ID = config('O2AUTH_CLIENT_ID')

O2AUTH_CLIENT_SECRET = config('O2AUTH_CLIENT_SECRET')

MONETBIL_SERVICE_KEY = config('MONETBIL_SERVICE_KEY')

RECAPTCHA_API_KEY = config('RECAPTCHA_API_KEY')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')

RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')

MONETBIL_API_URL = config('MONETBIL_API_URL')

# For the SESSION 
# settings.py

# Keep users logged in for a very long time, e.g., 5 years (in seconds)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 * 5  # 5 years

# Ensure the session does not expire when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Optional: Use database-based session engine to persist session data
SESSION_ENGINE = 'django.contrib.sessions.backends.db'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer', ),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', )
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.UserAccount'

LOGIN_URL = '/auth/signin'
LOGOUT_URL = '/'

# LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/auth/signin'

BASE_COUNTRY = 'CMR'
