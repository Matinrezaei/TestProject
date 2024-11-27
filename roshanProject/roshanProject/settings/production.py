from .base import *
import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_NAME', 'mat'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'Rc3ba9632qm'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
