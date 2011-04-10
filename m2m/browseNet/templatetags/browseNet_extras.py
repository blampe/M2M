from django import template

from datetime import datetime
from binascii import crc32

from browseNet.models import Path, Share
from search.models import File, Host
from search.templatetags.search_extras import makeLink

register = template.Library()

@register.filter
def linkit(object,directServe=False):
    """
    See :filter:`search_extras-makeLink`.
    """
    return makeLink(object,directServe)

@register.filter
def all(value,ordering="alph"):
    """
    Interface for objects.all; expects a :model:`browseNet.share` or :model:`browseNet.path`
    """
    # if they have no shares, don't try to see them!
    if len(value.all()) < 1:
        return ""
    if ordering == "alph":
        if isinstance(value.all()[0],Share):
            ordering = 'sharename'
        elif isinstance(value.all()[0],Path):
            ordering = 'shortname'
        else:
            ordering = 'pk'
    return value.all().order_by(ordering)

@register.filter
def sizeToReadable(value):
    '''
    Takes a number of bits and reformats it to nice MB/GB/TB format.
    Intelligently handles different models
    '''
    if isinstance(value,Share):
        value = value.totalfilesize
    elif isinstance(value,Path):
        value = value.pathsize
    elif isinstance(value,File):
        value = value.filesize
    elif isinstance(value,Host):
        value = value.totalfilesize
    else:
        return "??"
    if value < 0:
        return "??"
    value = float(value)
    count = 0
    while value > 1024:
        value = value/1024
        count += 1
        
    if count == 1:
        appender = "KiB"
    elif count == 2:
        appender = "MiB"
    elif count == 3:
        appender = "GiB"
    elif count == 4:
        appender = "TiB"
    else:
        appender = "B"
        
    niceNum = "%.1f" % value
    
    return niceNum + " " + appender

@register.filter
def dateForm(value,format="%m/%d/%Y %H:%M"):
    '''
    customizes display of datetime, according to a supplied ``format`` or the default "%m/%d/%Y %H:%M"
    '''
    try:
        return value.strftime(format)
    except:
        try:
            #not a datetime object, probably a timestamp(BRYYYYYYCE)
            return datetime.fromtimestamp(float(str(value)))
        except ValueError:
            return "??"

@register.filter
def nameControl(value):
    '''deals with long names'''
    
    if len(value) > 27:
        value = value[:25]+"..."
    return value

@register.filter
def getName(value):
    """
    Finds the name of a :model:`browseNet.path` or :model:`browseNet.Share`.
    """
    if isinstance(value,Path):
        return value.shortname
    elif isinstance(value, Share):
        return value.sharename
    else:
        return "??"

@register.filter
def pathLink(value):
    """
    retuns a link to a :model:`browseNet.path` or :model:`browseNet.Share` or :model:`browseNet.Host`.
    """
    if isinstance(value,Path):
        return "%s%s" %(value.hid.ip,value.fullname)
    elif isinstance(value,Share):
        return "%s/%s" % (value.hostid.ip,value.sharename)
    elif isinstance(value, Host):
        return value.ip
    else:
        return ""

@register.filter
def findPID(value):
    """
    finds the PID of a :model:`browseNet.path` or :model:`browseNet.Share`.
    """
    # this is a share. Ugh.
    if isinstance(value,Path):
        return value.pid
    else:
        path = '/' + value.sharename
        hid = value.hostid.hid
        
        # old m2m used a hash:
        # hash = "%s"%binascii.crc32(bin(value.shareid)+bin(hid)+path)
        
        # I can't recreate bryce's hashes correctly yet, but selecting fullname instead works in the meantime.
        sharepath = Path.objects.get(hid=hid,sid=value.shareid,fullname=path)
        
        return sharepath.pid

