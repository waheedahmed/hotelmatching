import os
import sys
activate_this = '/home/rizwan/Django_V1.4/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
path = '/home/dev/hotel_matching'
sys.path.append('/home/dev/')
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hotel_matching.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
