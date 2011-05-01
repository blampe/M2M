from django.conf.urls.defaults import *


urlpatterns = patterns('faq.views',
    ('^servers','servers'),
    ('^','basic'),
    
    )