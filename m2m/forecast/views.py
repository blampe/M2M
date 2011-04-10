from django.template import Context, loader
from django.template import RequestContext
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
import os, re
from django.views.generic.list_detail import object_list, object_detail


import django.http as http
import django.shortcuts as shortcuts
import models

def current(request):
    return render_to_response('core/forecast_index.html', { }, context_instance = RequestContext(request))


