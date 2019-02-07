"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'izf@@s$cv&6#26t8)vhu5!^@^u^%vukyxr&a4&&^cqu89-!xms'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # django-allauth requirement

    # 3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'graphene_django',
    'webpack_loader',
    
    # local apps
    'costasiella.apps.CostasiellaConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 3rd party
    'graphql_jwt.middleware.JSONWebTokenMiddleware',

    # local apps
]

# Add GraphQL JWT Tokens
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # graphql JWT authorization
    'graphql_jwt.backends.JSONWebTokenBackend',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'costasiella',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Email configuration

EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525

# Graphene settings

GRAPHENE = {
    'SCHEMA': 'src.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

# Webpack loader

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.dev.json'),
        }
}

# Where to go after login, well... let's just go home and take care of things from there :).

LOGIN_REDIRECT_URL = 'home'

# Allauth configuration
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_REQUIRED = True # Users have to provide an email address when signing up
ACCOUNT_UNIQUE_EMAIL = False # Multiple users can have the same email address (eg. useful for customers who share their email addrress with partners)
ACCOUNT_EMAIL_VERIFICATION = "Mandatory" # Users have to verify their email address and can't login until it's verified
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 7
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900 # Lock out a user for 15 minutes after 7 invalid attempts to log in
ACCOUNT_USERNAME_BLACKLIST = [
    'admin'
]
ACCOUNT_USERNAME_MIN_LENGTH = 4 # At least 4 characters are required for the username