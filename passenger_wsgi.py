import os
import sys

# cPanel's Python App points here. Make sure the project root is on the path.
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oagroup.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
