from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def lenlimit(s, size):
    try:
        size = int(size)
    except:
        return u"??"
    s = str(s)
    if len(s) > size:
        s = u"{}...{}".format(s[:size/2],s[-size/2:])
    return s