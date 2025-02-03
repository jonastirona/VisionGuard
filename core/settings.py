import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'camera.apps.CameraConfig',
]

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

# filepath: /c:/Users/Jonas/OneDrive/Documents/repos/VisionGuard/core/settings.py
MIDDLEWARE = [
    # 'django_basic_auth_ip_whitelist.middleware.BasicAuthIPWhitelistMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'vision-guard.org'
]

BASIC_AUTH_LOGIN = 'admin'
BASIC_AUTH_PASSWORD = 'securepassword'
BASIC_AUTH_WHITELISTED_IP_RANGES = ['127.0.0.1/32']

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
ROOT_URLCONF = 'core.urls'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'