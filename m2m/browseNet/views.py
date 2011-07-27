from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Min,Max
from django.core.urlresolvers import reverse

from browseNet.models import Smb, Share, Path
from search.models import File, Host

import time
# Create your views here.


def listAll(request,page=1):
    '''
    Creates the paged listing of all servers with a size of 0 or greater.

    Arguments:
        page
            1-indexed
    Context:
        title
            M2M - Servers: Page {{page}}
        serverListing
            A list populated by  :model:`browseNet.Host`
        totalFound
            Number of servers found
        servers
            Marks the severs nab tab as current
        linkPages
            handles the pagination of the server list
        page
            1-indexed
        ordering
            Determines the order in which the servers are displayed.
    Templates:
        :template:`browseNet/list`
    '''
    PERPAGE = 20
    try:
        page = int(page) - 1 # switch to zero indexing
        if page < 0:
            page = 0
    except Exception:
        page = 0

    
    defaultOrdering = "hid__totalfilesize"
    director = '-'
    try:
        if request.GET['order'] != "": # empty arguments become the default.
            allowableOrderings = ["hid__totalfilesize","hid__lastscan","workgroup","hostname"]
            ordering = request.GET['order']
            if (ordering[0] == '-' and ordering[1:] in allowableOrderings):
                director = '-'
                ordering = ordering[1:]
            elif ordering in allowableOrderings:
                director = ''
            else: # unrecognized orderings become default also
                ordering = defaultOrdering
        else:
            ordering = defaultOrdering
    except KeyError: # and so do invalid keys
        ordering = defaultOrdering
    
    minReqd = ['hid__totalfilesize',]
    
    '''if ordering in minReqd:
        serverListing = Smb.objects.order_by("%s%s"%(director,ordering))
    else:'''
    serverListing = Smb.objects.order_by("%s%s"%(director,ordering))
        
    
    # get rid of no-size servers. Fuck those guys.
    serverListing = serverListing.filter(hid__totalfilesize__gte=0)
    
    
    totalFound = len(serverListing)
    serverListing = serverListing[page*PERPAGE:(page+1)*PERPAGE]
    
    
    remainder = totalFound % PERPAGE # we need to do this because setLen and PERPAGE are ints
    if remainder > 0:
        remainder = 1
    linkPages = range(1,totalFound/PERPAGE + remainder + 1)
    
    
    return render_to_response("browseNet/list.html",{
                                'title': "M2M - Servers: Page %d"%(page+1),
                                'serverListing':serverListing,
                                'totalFound':totalFound,
                                'servers':'current',
                                'linkPages':linkPages,
                                'page' : page + 1,
                                'ordering' : '%s%s'%(director,ordering),
                            },)

@transaction.autocommit    
def deepBrowse(request,type="Q",id=-1):
    """
    Shows the innards of a :model:`browseNet.Host`, :model:`browseNet.Share`, :model:`browseNet.Path`

    Templates: ``browseNet/deep.html``
    Context:
        servers
            Sets the server nav tab as current
        folder
            The current browsing :model:`browseNet.Path`
        folderlist
            A list of the folders held in the current browsing path
        filelist
            A list of the files held in the current browsing path
        ordering
            What order to display the files in
        host
            The parent :model:`browseNet.Host`
    """
    allowedTypes = ['H','S','P']
    id = int(id)

    try:
        request.GET['order']
        ordering = request.GET['order']
    except KeyError:
        ordering = 'alph'
        
    if type not in allowedTypes or id < 0:
        return HttpResponseRedirect(reverse('browseNet.views.listAll',args=(1,)))

    
    if type == "H":
        # this is a host list - we only need return the all of its highest-level shares.
        host = get_object_or_404(Host,pk=id)
        folder = host
        folderList = host.share_set.filter(totalfilesize__gte=1)
        
        #likewise, only files at the root
        rootPID = Path.objects.filter(hid=id,parent.pid=0).order_by('-pid')[0].pid # a host's root PID is gotten by matching its HID to a path with PPID = 0.
        fileList = File.objects.filter(path=rootPID)
    
    elif type == "S":
        # cry yourself to sleep.
        fileList = ''
        # since shares are root folders...we can find their path.
        folder = get_object_or_404(Share,pk=id)
        
        path = '/' + folder.sharename
        hid = folder.hostid.hid
        host = Host.objects.get(pk=hid)
        try:
            sharepath = Path.objects.get(hid=hid,sid=id,fullname=path)
            pid = sharepath.pid # phew
            fileList = File.objects.filter(path=pid)
            folderList = Path.objects.filter(parent.pid=pid, pid__gte=1)
        except: # sometimes a share has no path, due to permissions and shit
            folderList = ""
            fileList = ""
        
    elif type == "P":
        # this is the simplest to do. theoretically.
    

        folder = get_object_or_404(Path,pk=id)
        
        
        folderList = Path.objects.filter(parent=id, pid__gte=1)
        fileList = File.objects.filter(path=id)
        host = folder.hid
        
    else:
        return HttpResponseRedirect(reverse('browseNet.views.listAll',args=(1,)))
        
    #
    # ---- Logging Stuff ---- #
    #
        from django.db import connection

        cursor = connection.cursor()

        cursor.execute('LOCK TABLES log WRITE')
        cursor.execute(
            'INSERT INTO log (Time,Client,SearchString) VALUES (%(time)d, "%(client)s", "%(search)s")' % {
                'time':time.mktime(time.localtime()),
                'client': request.META['HTTP_X_FORWARDED_FOR'],
                'search':"Browse: %s, %d"%(type,id),
            }
        )
        cursor.execute('UNLOCK TABLES')
        transaction.set_dirty()
        transaction.commit()
        connection.close()
    ####################################
        
    return render_to_response("browseNet/deep.html",{
                                'servers':'current',
                                'folder':folder,
                                'folderList':folderList,
                                'fileList':fileList,
                                'ordering':ordering,
                                'host':host,
                            },)
