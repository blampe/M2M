import os
import sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

sys.path.append(workspace)

sys.path.append('/usr/lib/python2.6/dist-packages/django')
sys.path.append('/home/haak/django_projects/m2m')


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
