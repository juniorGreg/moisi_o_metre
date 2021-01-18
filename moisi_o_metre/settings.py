"""
Django settings for moisi_o_metre project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
import base64

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG'] == 'TRUE'

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "moisi-o-metre.herokuapp.com", "moisiometre.xyz"]

BULLSHIT_O_METRE_API = os.environ['BULLSHIT_O_METRE_API']

#Encode printful api key in base64
data = os.environ['PRINTFUL_API_KEY']
urlSafeEncodedBytes = base64.urlsafe_b64encode(data.encode("utf-8"))
urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")

PAYPAL_SANDBOX_CLIENT_ID=os.environ["PAYPAL_SANDBOX_CLIENT_ID"]
PAYPAL_LIVE_CLIENT_ID=os.environ["PAYPAL_LIVE_CLIENT_ID"]


PRINTFUL_API_KEY = urlSafeEncodedStr

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    "blog.apps.BlogConfig",
    "bullshit_o_metre.apps.BullshitOMetreConfig",
    "store.apps.StoreConfig",
    "storages",
    'django.contrib.sites',
    'django.contrib.sitemaps'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]


ROOT_URLCONF = 'moisi_o_metre.urls'

SITE_ID = 1

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

WSGI_APPLICATION = 'moisi_o_metre.wsgi.application'
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 2592000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),

    }
}

import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600)



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

LANGUAGE_CODE = 'fr-ca'

TIME_ZONE = 'America/Montreal'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%d %m %Y %H:%M'

}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= (
            'rest_framework.renderers.JSONRenderer',
        )








#Email settings
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_ADMIN = os.environ['EMAIL_ADMIN']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#config aws bucket

if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = True
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_REGION_NAME = "us-east-2"
    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

    DEFAULT_FILE_STORAGE = 'moisi_o_metre.storage_backends.PublicMediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/images/'
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/images/'
    MEDIA_ROOT= os.path.join(BASE_DIR, 'static/images')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]



django_heroku.settings(locals(), staticfiles=False)
