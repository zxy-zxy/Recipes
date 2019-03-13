from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db', 'db.sqlite3'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'sql.log',
        },
    },
    'loggers': {
        'django.db.backends': {'handlers': ['console', 'file'], 'level': 'DEBUG'}
    },
}

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
