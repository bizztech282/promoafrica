"""
WSGI config for app.
"""
import os
from django.core.wsgi import get_wsgi_application

# Default to production if not set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.production')

application = get_wsgi_application()
