from stats.models import Log, Status, Status2
from django.contrib import admin

class StatusAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':('lastchange','id','files','directories','queries',)})
    ]
    
    list_display = (
                    'lastchange',
                    'smbhosts',
                    'queries',
                    'files',
                    'directories',
                    )
    
#    list_filter = ('id','lastchange',)
    
admin.site.register(Status,StatusAdmin)

class Status2Admin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':('time','id','queries','onlinehosts',)})
    ]
    
    list_display = (
                    'time',
                    'queries',
                    'onlinehosts',
                    )
    
    list_filter = ('time',)
    
admin.site.register(Status2,Status2Admin)