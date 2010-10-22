import os
import sys

path = '/srv/taglife'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
