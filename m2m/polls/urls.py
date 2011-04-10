from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from polls.models import Poll

urlpatterns = patterns('polls.views',
    (r'^$',
        'index'),
    url(r'^(?P<pk>\d+)/$', 
        DetailView.as_view(
            model=Poll,
            template_name="polls/detail.html"
            ),
        name='poll_detail'
        ),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='polls/results.html',
            ),
        name='poll_results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)