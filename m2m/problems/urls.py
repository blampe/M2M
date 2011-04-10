from django.conf.urls.defaults import *

# Urls go here!

urlpatterns = patterns('problems.views',
        (r'^.*','sitewide'),
        (r'^requests','requests'),
        (r'^stats','stats'),
        (r'^news','news'),
        (r'^servers','browseNet'),
        (r'^polls','polls'),
    )