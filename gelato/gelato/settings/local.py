# -*- coding: UTF-8 -*-

"""Development settings and globals."""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from base import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
#See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    #
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'gelato',
    #     'USER': 'gelato',
    #     'PASSWORD': 'toto123',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION
# See : http://blog.pilotsystems.net/2011/juin/utilisation-south-application-django-migrations-versions-base-donnees-schema

INSTALLED_APPS += (
    'django_extensions',
)