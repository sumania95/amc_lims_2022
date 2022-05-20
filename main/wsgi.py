import os
import sys
from django.core.wsgi import get_wsgi_application
from pathlib import Path

# Add project directory to the sys.path
path_home = str(Path(__file__).parents[1])
if path_home not in sys.path:
	sys.path.append(path_home)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()
