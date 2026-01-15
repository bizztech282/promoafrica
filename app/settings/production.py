from .base import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'promoskiza.onrender.com').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    ALLOWED_HOSTS = ['.onrender.com']

# Security
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database
# Safely get database URL, default to sqlite if missing (though Render should provide it if added)
# or if they are using cookie session only, maybe they don't care about DB persistence much.
# But for production readiness, we check env.
if 'DATABASE_URL' in os.environ:
    db_from_env = dj_database_url.config(conn_max_age=500, ssl_require=True)
    DATABASES['default'].update(db_from_env)
