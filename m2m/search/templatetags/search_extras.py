from django import template
from django.utils.safestring import mark_safe

from datetime import datetime
import re

from search.models import File
from browseNet.models import Path

import urllib2

register = template.Library()

@register.filter
def sizeToReadable(value):
    '''
    Takes a number of bits and reformats it to nice MB/GB/TB format. Returns '??' in a pinch.

    Arguments:
        value
            Something that can be converted to float.
    '''
    try:
        value = float(value)
    except Exception:   # we expect a number, after all.
                        #or something that can be turned into a number.
        return "??"
    
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
        
    niceNum = "%.1f" % value # 1 decimal place for table formatting reasons
    
    return niceNum + " " + appender


@register.filter
def dateToReadable(value):
    '''
    converts that ugly fucking date to month/day format; expects a datetime object as an arg
    '''
    try:
        return value.strftime("%m/%d")
    except Exception:
        return "??"

@register.filter
def highlight(object,words, autoescape=None):
    '''bolds the search query in the files found in the search'''
    try:
        value = object.filename
    except AttributeError:
        value = object.fullname
    except:
        return object
    # REGULAR EXPRESSION MATCHING FOR HIGHLIGHTING SHIT
    for word in words:
        regexps = re.compile("("+word+")",flags=re.IGNORECASE) # generate a regexp WITH wrapping parens
        explosion = re.split(regexps,value)                    # the parens make this keep the match in the split list
        expl2 = []
        for piece in explosion: # oh gods please work
            if re.match(regexps,piece):
                piece = "<b>"+piece+"</b>" # this doesn't change the piece inside of explosion...
            expl2 += [piece]               # so fuck it. we'll just populate a new list!
        value = ''.join(expl2)
        
    return mark_safe(value)
highlight.is_safe = True

@register.filter
def makeLink(object, directServe=False):
    ''' 
    Intelligently returns the link to a file or path, either smb or http, based on the parameter directServe. If True, creates a direct link. If false, creates an smb link ref.
    '''
#    if isinstance(object, File)
    try:
        if object.path.hid.servesDirect == True and directServe != False:
            return "http://%s:%d%s/%s" % (object.path.hid,object.path.hid.directPort, urllib2.quote(str(object.path)),urllib2.quote(str(object)))
        else:
            return "smb://%s%s" % (object.path.hid, object.path)
    except AttributeError: # no object.path -> object is a path
        if object.hid.servesDirect == True and directServe != False:
            '''do nothing'''
        return "smb://%s%s" % (object.hid, object)
    except:
        return "??"

@register.filter
def host(object):
    '''
    Returns the :model:`browseNet.Host` of a :model:`browseNet.Path` or :model:`search.File`, or '??' if it can't for any reason.
    '''
    try:
        return object.hid
    except AttributeError:
        return object.path.hid
    except:
        return '??'
    
@register.filter    
def size(object):
    ''' 
    returns the size of the :model:`browseNet.Path` or :model:`search.File`
    '''
    try:
        return object.filesize
    except AttributeError:
        return object.pathsize
    except:
        return '??'
    
