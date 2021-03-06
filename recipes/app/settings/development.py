from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipes_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'recipes-db',
        'PORT': 5432,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'}},
}

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'
