from polls.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    can_delete = False

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields':['question']}),
        ('Date Information',    {'fields':['pub_date'], 'classes':['collapse']}),
    ]
    
    list_display = ('question','pub_date','was_published_today')
    list_filter = ['pub_date']
    
    search_fields = ['question']
    
    date_hierarchy = 'pub_date'
    
    
    inlines = [ChoiceInline]

admin.site.register(Poll,PollAdmin)