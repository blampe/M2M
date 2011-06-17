from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView


urlpatterns = patterns('imaging.views',
    (r'^$', 'bad_request'),
    (r'^movie/no_poster/(?P<id>\d+)','no_poster'),
    )