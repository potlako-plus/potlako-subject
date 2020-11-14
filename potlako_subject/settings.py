"""
Django settings for potlako_subject project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = 'potlako_subject'

SITE_ID = 1

ETC_DIR = os.path.join(BASE_DIR, 'etc')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1et5jcq@=j*0+z*q%h8a+0s^qv^1auhbwow73&wc$4pr-wji2d'

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
    'django.contrib.sites',
    'django_crypto_fields.apps.AppConfig',
    'django_extensions',
    'rest_framework.authtoken',
    'edc_action_item.apps.AppConfig',
    'edc_sync.apps.AppConfig',
    'edc_sync_files.apps.AppConfig',
    'edc_base.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_identifier.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_reference.apps.AppConfig',
    'edc_metadata_rules.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'potlako_metadata_rules.apps.AppConfig',
    'potlako_visit_schedule.apps.AppConfig',
    'potlako_reference.apps.AppConfig',
    'potlako_prn.apps.AppConfig',
    'potlako_subject.apps.EdcAppointmentAppConfig',
    'potlako_subject.apps.EdcFacilityAppConfig',
    'potlako_subject.apps.EdcMetadataAppConfig',
    'potlako_subject.apps.EdcProtocolAppConfig',
    'potlako_subject.apps.EdcDeviceAppConfig',
    'potlako_subject.apps.EdcVisitTrackingAppConfig',
    'potlako_subject.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',
]

ROOT_URLCONF = 'potlako_subject.urls'

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

WSGI_APPLICATION = 'potlako_subject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
     },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
     },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
     },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

DATE_INPUT_FORMATS = ['%d-%m-%Y']

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True

USE_L10N = False

USE_TZ = True

COUNTRY = 'botswana'

# dashboards
DASHBOARD_URL_NAMES = {
    'subject_listboard_url': 'potlako_dashboard:subject_listboard_url',
    'screening_listboard_url': 'potlako_dashboard:screening_listboard_url',
    'subject_dashboard_url': 'potlako_dashboard:subject_dashboard_url',
}

HOLIDAY_FILE = os.path.join(BASE_DIR, 'holidays.csv')
CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$|^[2-8]{1}[0-9]{6}$'

EDC_SYNC_SERVER_IP = None
EDC_SYNC_FILES_USER = None
EDC_SYNC_FILES_REMOTE_HOST = None
EDC_SYNC_FILES_USB_VOLUME = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

if 'test' in sys.argv:

    class DisableMigrations:

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
