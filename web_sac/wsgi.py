"""
WSGI config for web_sac project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if we're running in Docker environment
if os.environ.get('DJANGO_SETTINGS_MODULE'):
    # Use the already set settings module (from Docker ENV)
    pass
else:
    # Use default settings for development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_sac.settings')

application = get_wsgi_application()
