from forecast.models import Forecast
from django.contrib import admin


class ForecastAdmin(admin.ModelAdmin):
        fields = [ 'partner_id', 'key', 'location_id' ]
        list_display = [ 'partner_id', 'key', 'location_id' ]

admin.site.register(Forecast, ForecastAdmin)

