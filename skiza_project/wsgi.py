"""
WSGI config for skiza_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skiza_project.settings')

# Auto-migrate for ephemeral environments (Render Free Tier)
from django.core.management import call_command
try:
    call_command('migrate')
except Exception as e:
    print(f"Migration failed: {e}")

application = get_wsgi_application()
