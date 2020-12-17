import os

from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', os.getenv('ENV', 'production') != 'production')

INSTALLED_APPS = [
    'db',
]

if DEBUG or not os.getenv('DATABASE_URL', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', 5432),
            'NAME': os.getenv('DB_NAME', 'remy_db'),
            'USER': os.getenv('DB_USER', 'remy'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
        }
    }
else:
    DATABASES = {'default': os.getenv('DATABASE_URL')}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
