"""
WSGI config for bui_transport project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bui_transport.settings')

application = get_wsgi_application()