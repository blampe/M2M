from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from advancedsearch.models import *
from problems.models import *
from browseNet.models import Path



register = template.Library()

class DeleteNode(template.Node):
    
    
    def __init__(self, model, id, id_var):
        self.id_var = id_var
        self.model = model
        
    def render(self, context):
        try:
            target = self.id_var.resolve(context)
            self.target = globals()[self.model].objects.get(pk=int(target))
        except:
            raise ObjectDoesNotExist("Could not find a %r with id %r" % (globals()[self.model],self.id_var.resolve(context)))
        
        self.target.delete()
        
        return ''
        
@register.tag(name="delete")
def do_delete(parser,token):
    try:
        tag_name, model, id = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError ("%r tag requires two arguments" % token.contents.split()[0])
    try:
        id_var = template.Variable(id)
    except:
        raise ValueError("Could not understand the id %r" % id)
    return DeleteNode(model,id,id_var)
    
