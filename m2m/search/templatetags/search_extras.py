from django import template
from django.utils.safestring import mark_safe

from datetime import datetime
import re

from search.models import File
from browseNet.models import Path

from basic.blog.models import Post

import urllib2

register = template.Library()
@register.filter
def order_by(queryset, args):
    '''
    Orders a queryset
    
    Arguments:
        queryset
            duh
        args
            a string of attributes by which to order, separated by commas
    '''
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

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
    
    if len(value) > 105: 
        value = value[:35] + "..." + value[-35:]

    
    # REGULAR EXPRESSION MATCHING FOR HIGHLIGHTING SHIT
    for word in words:
        regexps = re.compile("("+word+")",flags=re.IGNORECASE) # generate a regexp WITH wrapping parens
        explosion = re.split(regexps,value)                    # the parens make this keep the match in the split list
        expl2 = []
        for piece in explosion: # oh gods please work
            if re.match(regexps,piece):
                piece = "<strong>"+piece+"</strong>" # this doesn't change the piece inside of explosion...
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
        try:
            if object.hid.servesDirect == True and directServe != False:
            #do nothing
                return "smb://%s%s" % (object.hid, object)
            else:
                return "smb://%s%s" % (object.hid, object)
        except AttributeError:
            try:
                # no HID - shouldn't exist anymore anyway.
                object.delete()
            except:
                pass
            return "??"
    except:
        return "??"

@register.filter
def sanitize(file):
    ''' Returns a UnicodeEncodeError safe string. Fuck these template errors.'''
    
    try:
        string = file.filename.encode('ascii','replace')
    except:
        string = "??"
    return string
        
@register.filter
def host(object):
    '''
    Returns the :model:`browseNet.Host` of a :model:`browseNet.Path` or :model:`search.File`, or '??' if it can't for any reason.
    '''
    try:
        return object.hid
    except AttributeError:
        try:
            return object.path.hid
        except:
            return '??'
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


@register.filter
def status(object):
    ''' prints good/bad/unclear image for file'''
    try:
        object.pathsize
        return ''
    except AttributeError:
        img = "<img class='statusind' style=\"float:right;margin-right:15px;\" src='/media/images/%(img)s' alt='%(alt)s'/>"
        if object.goodfile == 1:
            value = img % {'img':'goodfile.gif','alt':'File is good!'}
        elif object.goodfile == 0:
            value = img % {'img':'badfile.gif','alt':'File is bad.'}
        else:
            value = img % {'img':'goodfile.gif','alt':'File is contested.'}
        return mark_safe(value)
    except:
        return ''
status.is_safe=True
        
################################################################
#  Handler for {% logo %} tag
#
from django.core.urlresolvers import reverse
import random
class LogoNode(template.Node):
    
    mChoices = ['Mmath'] * 15 # make it more likely to see the old M's
    mChoices += ['Moldenglish',
                'Mvivaldi',
                'Mcurlz',
                'Mmagneto',
                'M_andrew_ho']
    arrows = ['Arrowmath'] * 10 # also the old arrow
    
    styling = "<a class='logolink' href=\"%s\">\
                <div id='modlogo' style=\"\">%s</div>\
                </a>"
    
    extras = {
        'movies':styling % (reverse('advancedsearch.views.movieSplash'),'ovies'),
        'music': styling % (reverse('advancedsearch.views.musicSplash'),'usic'),
        'shows': styling % (reverse('advancedsearch.views.showSplash'),'TV'),
        'None':"",
    }
    
    def __init__(self, module):
        
        # halloween!
        if (datetime.now().day in [29,30,31] and datetime.now().month==10):
            self.left = 'mPunkin'
            self.right = 'mHalCat'
            self.arrow = 'Arrowmath'
        else:
            self.left = random.choice(self.mChoices)
            self.right = random.choice(self.mChoices)
            self.arrow = random.choice(self.arrows)
        
        # jessi peck's birthday
        if (datetime.now().day == 25 and datetime.now().month == 10):
            self.left = 'M_jessi_peck'
            
        if module not in self.extras:
            raise ValueError("logo tag could not recognize module: %r" % module)
        else:
            self.extra = self.extras[module]
    def render(self, context):
        try:
            return "\
            <a href=\"%(index)s\"><span>\
                        <img  id='leftlogo' src='/media/images/%(left)s.png'/>\
                        <img  id='arrowlogo' src='/media/images/%(arrow)s.png'/>\
                        <img  id='rightlogo' src='/media/images/%(right)s.png'/></span></a>%(extra)s" % {
                                                                                    'left':self.left,
                                                                                    'right':self.right,
                                                                                    'arrow':self.arrow,
                                                                                    'extra':self.extra,
                                                                                    'index':reverse('search.views.index')
                                                                                    }
        except:
            return '<span style="font-size:6em;">Logo Unavailable</span>'
            
@register.tag(name="logo")
def do_logo(parser,token):
    try:
        tag_name, module = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError ("%r tag requires an argument" % token.contents.split()[0])
    return LogoNode(module)
#
################################################################

@register.tag(name="extra_styles")
def do_extra_styles(parser,token):
    return ExtraStyles()
    
class ExtraStyles(template.Node):
    def __init__(self):
        # halloween!
        self.stylesheet = []
        if (datetime.now().day in [29,30,31] and datetime.now().month == 10):
            self.stylesheet += ['halloween']
    
    def render(self, context):
        if self.stylesheet == []:
            return ''
        else:
            return '\n'.join(["<link rel=\"stylesheet\" type=\"text/css\" href=\"/media/styles/{}.css\" />".format(x) for x in self.stylesheet])


from datetime import date, timedelta

class NewNewsNode(template.Node):
    string = "<div id=\"newNews\"><p>+{:d}</p></div>"
    
    def __init__(self, *args, **kwargs):
        self.number = Post.objects.filter(publish__gt=date.today()-timedelta(days=4)).count()
        
    def render(self, context):
        try:
            if self.number > 0:
                return self.string.format(self.number)
            else:
                return ""
        except:
            return ""
            
@register.tag(name="latestnews")
def do_newNews(parser,token):
    try:
        tag_name = token.split_contents()
    except:
        return ""
    return NewNewsNode()
