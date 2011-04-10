from django.conf.urls.defaults import *
from django.views.generic.list_detail import *


urlpatterns = patterns('',
    (r'^current/$', 'testpro.forecast.views.current'),
)
