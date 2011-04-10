from django import template
from testpro.forecast.weather import Weather
from testpro.forecast.models import Forecast
from django.core.cache import cache
from django.conf import settings

register = template.Library()

def get_condision(): 
    f = Forecast.objects.get(id=1)
    is_cached = "false"
    ws = cache.get('ws')

    if ws == None:
	    ws = Weather(f.partner_id, f.key, f.location_id)
	    cache.set('ws', ws, 120)
    else:
	is_cached = "true"
    return {'rt': ws.rt, 'cached': is_cached, 'ws': ws, 'media_url': settings.__getattr__('MEDIA_URL')}


register.inclusion_tag('forecast/forecast_condision.html')(get_condision)
