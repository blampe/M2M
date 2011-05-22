from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('movies.views',
    (r'^$', 'splash'),
    
    
    )