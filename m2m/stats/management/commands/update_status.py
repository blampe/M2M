from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum

import datetime

from m2m.stats.models import Status, Status2
from m2m.search.models import File
from m2m.browseNet.models import Path


class Command(BaseCommand):
    args = ''
    help = "creates a new row in the status table. every day."
    
    def handle(self, *args, **kwargs):
        lastStatus = Status.objects.latest('lastchange')
        Status.objects.create(
                              lastchange=datetime.datetime.now(),
                              smbhosts=lastStatus.smbhosts,
                              ftphosts=lastStatus.ftphosts,
                              directories=Path.objects.all().count(),
                              files=File.objects.all().count(),
                              filesize=File.objects.all().aggregate(Sum('filesize'))['filesize__sum'],
                              queries=lastStatus.queries,
                              updatinghost=0
                              )
        
