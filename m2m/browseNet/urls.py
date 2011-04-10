from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('browseNet.views',
        
        (r'^(?P<type>[HPS])/(?P<id>\d+)','deepBrowse'),
        (r'^(?P<page>\d*)','listAll'),
        
    )