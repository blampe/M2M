from django.conf.urls.defaults import *


urlpatterns = patterns('faq.views',
    (r'^servers','servers'),
    (r'^','basic'),
    )