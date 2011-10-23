from django.conf.urls.defaults import *
#from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from datetime import datetime

urlpatterns = patterns('',
    # Example:
    # (r'^m2m/', include('m2m.foo.urls')),
    #(r'^api/v1/', include('fiber.api.urls')),
    #(r'^admin/fiber/', include('fiber.admin_urls')),
    #(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('fiber',),}),
    (r'^flat', include('django.contrib.flatpages.urls')),
    (r'^tos', 'faq.views.serviceTerms'),
    (r'^dmca', 'faq.views.dmca'),
    #(r'^', 'problems.views.sitewide'), # for maintenance, etc
    (r'^imaging/',include('imaging.urls')),
    (r'^monkeybutter$', 'search.views.test'),
    
    (r'^$', 'search.views.index'),
    #(r'^?q=([a-zA-Z0-9]*)$','search.views.results' ),
    (r'^search/', include('search.urls')),
    (r'^advanced/', include('advancedsearch.urls')),
    #(r'^requests', 'problems.views.requests'), # for maintenance, etc
    (r'^requests/', include('requests.urls')),
    
    (r'^polls', 'problems.views.polls'), # for maintenance, etc
    (r'^polls/', include('polls.urls')),
    
    #(r'^servers', 'problems.views.browseNet'), # for maintenance, etc
    (r'^servers/', include('browseNet.urls')),
    
    #(r'^(news|comments)/', 'problems.views.news'), # for maintenance, etc
    (r'^news/', include('basic.blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (r'^problems/', include('problems.urls')),
    
    (r'^stats', 'problems.views.stats'), # for maintenance, etc
    (r'^stats/', include('stats.urls')),

    (r'^faq&', 'faq.views.basic'),
    (r'^faq/', include('faq.urls')),
    

    
    (r'^about/m2m$','faq.views.about',{'typeof':'m2m'}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)

#if settings.DEBUG:
#    urlpatterns += patterns('django.contrib.staticfiles.views',
#        url(r'^static/(?P<path>.*)$', 'serve'),
#    )