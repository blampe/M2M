from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('search.views',
    (r'^$', 'results'),
    (r'^(?P<page>\d+)','results'),
    (r'^test$','test'),
    
    
    )