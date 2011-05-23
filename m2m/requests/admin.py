from requests.models import Comment
from django.contrib import admin


def markDeleted(modeladmin,request,queryset):
    queryset.update(isDeleted=True)
markDeleted.short_description = "Mark selected requests as deleted"
def markDeleted(modeladmin,request,queryset):
    queryset.update(isDeleted=False)
markDeleted.short_description = "Mark selected requests as not deleted"

class CommentAdmin(admin.ModelAdmin):
    
    list_display = (
                    'CID',
                    'requestTime',
                    'request',
                    'isDeleted',
                    'completed',
                    'completedTime',
                    'completingServer',
                    'requestIP',
                    )
    
    list_filter = ['requestTime',
                   'completedTime',
                   'completed',
                   'isDeleted',
                   'completingServer',]
    
    search_fields = ['request','completingServer']
    
    date_hierarchy = 'requestTime'
    
    actions = [markDeleted]

admin.site.register(Comment,CommentAdmin)
#admin.site.register(Comments,CommentsAdmin)
