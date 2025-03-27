import os
from pathlib import Path
from .settings import *

# Load environment variables
import dotenv
dotenv.load_dotenv()

# Get the environment variables
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
DEBUG = os.environ.get('DEBUG', '0') == '1'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Use SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
    }
}

# Ensure the database directory exists
os.makedirs(os.path.join(BASE_DIR, 'db'), exist_ok=True)

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Remove or update STATICFILES_DIRS to point to an existing directory
# Comment out the original STATICFILES_DIRS from settings.py
STATICFILES_DIRS = []  # Empty list to override the setting from settings.py

# WhiteNoise middleware for static files in production
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 