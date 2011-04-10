from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('search.views',
    (r'^test$','test'),
    (r'^(?P<page>\d*)','results'),
    
    )