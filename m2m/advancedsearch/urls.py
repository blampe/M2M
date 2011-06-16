from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('advancedsearch.views',
    (r'^$', 'splash'),
    (r'^movies/?$', 'movieSplash'),
    (r'^movies/results/?$', 'movieSearch'),
    (r'^movies/results/(?P<page>\d+)','movieSearch'),
    (r'^movies/details/(?P<id>\d+)','movieDetail'),
    (r'^movies/random/$','movieRandom'),
    (r'^shows$', 'showSplash'),
    
    (r'^music$', 'musicSplash'),
    
    )