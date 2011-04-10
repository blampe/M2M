from browseNet.models import Host,Smb
from django.contrib import admin
  
class HostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':('ip','hosttype','expirecount','period',
                          'counter','networkaddress','servesDirect','flags')})
    ]
    
    list_display = (
                    'smb',
                    'hid',
                    'ip',
                    'totalfilesize',
                    'networkaddress',
                    'servesDirect',
                    )
    
    list_filter = ('servesDirect','flags',)
    
    def queryset(self,request):
        qs = super(HostAdmin, self).queryset(request)
        # only show hosts with some size greater than -1:
        return qs.filter(totalfilesize__gte=0)


admin.site.register(Host,HostAdmin)
