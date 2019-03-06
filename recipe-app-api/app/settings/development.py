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
