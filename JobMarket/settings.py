"""
Django settings for JobMarket project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd8$)q+*^=*(5@8b+n&er%1_16*#%-xdlww5npwti^#5+mt0-t)'

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
    'market',
    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JobMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'JobMarket.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase',
#     }
# }

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# hostname = os.environ['DBHOST']
# which we construct using the DBHOST value.
# POSTGRES
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.path.join(BASE_DIR, 'db'),
#         'HOST': "django-job-site-postgresdb.postgres.database.azure.com",
#         'USER': "denisYakovliev@django-job-site-postgresdb",
#         'PASSWORD': "Ws1Dden19sen4O"
#     }
# }

# AZURE SQL Database
# DATABASES = {
#     'default': {
#          'ENGINE': 'sql_server.pyodbc',
#          'NAME': os.environ['DBNAME'],
#          'USER': os.environ['DBUSER'],
#          'PASSWORD': os.environ['DBPASS'],
#          'HOST': os.environ['DBSERVER'],
#          'PORT': '1433',
#          'OPTIONS': {
#              'driver': 'ODBC Driver 17 for SQL Server',
#              'MARS_Connection': 'True',
#         }
#     }
# }

DATABASES = {
    'default': {
         'ENGINE': 'sql_server.pyodbc',
         'NAME': 'database-cloudcomputing4',
         'USER': 'sampleLogin',
         'PASSWORD': 'samplePassword123!',
         'HOST': 'server-cloudcomputing4.database.windows.net',
         'PORT': '1433',
         'OPTIONS': {
             'driver': 'ODBC Driver 17 for SQL Server',
             'MARS_Connection': 'True',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

AUTH_USER_MODEL = "accounts.user"