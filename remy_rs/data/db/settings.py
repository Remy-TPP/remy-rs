import os

from dotenv import load_dotenv
load_dotenv()
import dj_database_url  # noqa: E402


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', os.getenv('ENV', 'production') != 'production')

INSTALLED_APPS = [
    # hacky but allows all this to work whether it be imported locally or from project root
    # values it will take: 'db', 'remy_rs.data.db'
    os.getenv('DB_APP_NAME', 'remy_rs.data.db'),
]

DB_URL = os.getenv('REMY_API_DB_URL', os.getenv('DATABASE_URL'))
if not DB_URL:
    print('Using DB_* env vars')
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
    print('Using REMY_API_DB_URL env var')
    DATABASES = {
        'default': dj_database_url.parse(DB_URL)
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
