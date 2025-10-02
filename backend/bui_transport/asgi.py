"""
ASGI config for bui_transport project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bui_transport.settings')

application = get_asgi_application()