from django import template
from django.template.defaultfilters import stringfilter
from django.shortcuts import get_object_or_404

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from datetime import datetime
import re #regexp shit

from browseNet.models import Smb
from requests.models import Comments

from basic.blog.templatetags.blog import formatBody

register = template.Library()

@register.filter
def dateSlice(value):
    '''chops off the extra date info'''
    return '%(month)s/%(day)s/%(year)s'%{'month':'%0*d'%(2,value.month),'day':'%0*d'%(2,value.day),'year':value.year}
    
@register.filter
def toHTML(value, autoescape=None):
    '''converts comments text to HTML'd text'''
    
    # use the same targets as the news posts
    return formatBody(value)
toHTML.is_safe = True
    
@register.filter
def hid(value):
    '''
    Creates a link to the completing/requesting server. expects a hostname.
    '''
    try:
        value = str(value)
    except:
        return "0"
    
    try:
        hoster = Smb.objects.filter(hostname=value)[0]
        return hoster.hid.hid
    except:
        return "0"
    
    
