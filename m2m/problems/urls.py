from django.conf.urls.defaults import *

# Urls go here!

urlpatterns = patterns('problems.views',
        
        (r'^requests','requests'),
        (r'^stats','stats'),
        (r'^news','news'),
        (r'^servers','browseNet'),
        (r'^host/(?P<id>\d+)','host'),
        (r'^polls','polls'),
        (r'^','sitewide'),
    )