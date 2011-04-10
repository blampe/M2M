from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('stats.views',
        
        (r'^','display'),
    )