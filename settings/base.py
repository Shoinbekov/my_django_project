"""
Django settings for shop project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-t=5c3djx02a)54yv2autvqh9#wfa@7r&l8fsvge^mni30z!r!1'

DEBUG = True

ALLOWED_HOSTS = []


# -----------------------------------------
# INSTALLED APPS
# -----------------------------------------

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Swagger (drf-spectacular)
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Third-party
    'rest_framework',
    'django_filters',

    # Local app
    'apps.core',
]


# -----------------------------------------
# MIDDLEWARE
# -----------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'settings.urls'


# -----------------------------------------
# TEMPLATES
# -----------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'settings.wsgi.application'

# -----------------------------------------
# DATABASE
# -----------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------------------
# PASSWORD VALIDATORS
# -----------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------------------------
# STATIC
# -----------------------------------------

STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------
# CUSTOM USER
# -----------------------------------------

AUTH_USER_MODEL = 'core.User'


# -----------------------------------------
# UNFOLD ADMIN
# -----------------------------------------

UNFOLD = {
    "SITE_HEADER": "E-Commerce Admin",
    "SITE_TITLE": "E-Commerce Admin",
    "SITE_SYMBOL": "💻",
}


# -----------------------------------------
# DRF + JWT + SPECTACULAR
# -----------------------------------------

REST_FRAMEWORK = {
    # JWT auth
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # ✔ Чтобы без токена давало 401, а не 403
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    # JSON only
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # Filtering
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    # Swagger schema
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "E-Commerce API",
    "DESCRIPTION": "API documentation for Midterm + Endterm project",
    "VERSION": "1.0.0",
}
