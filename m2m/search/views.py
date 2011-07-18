from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.db import transaction

from djangosphinx.apis.api278 import *
#from djangosphinx.manager import SphinxQuerySet

from search.models import File
from browseNet.models import Path
from stats.models import Status, Log


import re, time
from datetime import datetime

DEBUG = False
PERPAGE = 50

def test(request):
    """
    a place to do whatever the fuck needs to be done

    Templates: ``test.html``
    Context: 
        title
            The title of the page itself; not very useful for this one.
        debug
            Holds the specific things that are begin tested.
    """
    debug = {}

    debug['session'] = request.session
    
    return render_to_response('test.html',
                              {
                                'title':'M2M - TEST',
                                'debug':debug,
                              })

def index(request):
    """
    Just handles the root of the website. Nothing too complicated here.
    Primarly redirects to :view:`search.views.results` when used. Also displays
    the site messges of welcome/the day.

    Templates: ``base_page.html``
    Context:
        title
            Title of the page - "M2M - Search".
        search
            Marks this nav item as "current".
        debug
            boolean, prints out extra information if true.
    """
    # for april fools
    if datetime.now().day == 1 and datetime.now().month==4:
        from aprilfools.views import yearcaller
        return yearcaller(request)
    return render_to_response('base_page.html',
                              {
                                'title':"M2M - Search",
                                'search':'current',
                                'debug':DEBUG,
                               })
    
    
@transaction.autocommit
def results(request,page='1'):
    """
    Returns the formatted results of a search.
    
    Arguments:
        Page (optional)
            An int or string, denoting which page of results to show (0-indexed)
    
    Template: :template:`search/results`

    Context:
        title
            'M2M - Results: page {{page}}'
        search
            marks nav tab as 'current'
        q
            query string
        filesfound
            list of :model:`search.File`
        words
            list of the space-separated elements of {{q}}, used in :filter:`search_extras-highlight`
        params
            Keys:
                type
                    Which types of files were searched, by fileending
                mode
                    Which index(es) got searched
                order
                    How the results are to be sorted
                useip
                    This is not used anywhere.
        optionsUp
            A boolean, telling whether the options buttons are shown
        test
            Debugging variable
        page
           Current page number of results(1-indexed)
        prev
            previous page number of results (1-indexed)
        next
            Next page number of results (1-indexed)
        paginator
            A list of page numbers to show in the page links
        debug
            A dict of debugging stuff
        fileErrors
            An int counting the number of rows that couldn't be pulled out of the database
        errorids
            The id's of the :model:`search.File` s which caused errors 
        time
            Time it took to complete the search, in seconds
        total
            Total number of files found, up to :setting:`SPH_MAX_RESULTS`
        mode
            Shortcut to params['mode']
    """
    '''
        Handling some initial errors
    '''
    escape_chars = {
                    '!':r'\!',
                    '<':r'\<',
                    '>':r'\>',
                   # '(':r'\(',     # this is an operator for something
                   # ')':r'\)',     # this is an operator for something
                   # '@':r'\@',     # this is an operator for something
                    '~':r'\~',
                    "'":r'\'',
                    '"':r'\"',
                    '\\':r"",
                    '/' : r'\/',
                    #'$':r'$',
                    '%':"",
                    '#':'',
                    #'^':'%%5E',    # this is an operator for something
                    #'-':r'\-',     # this is an operator for something
                    #r'|':"%%7F",   # this is an operator for something
                    }
    try:
        q = request.GET['q']
        
        # april fools queries
        if datetime.now().day == 1 and datetime.now().month==4:
            from aprilfools.views import resultcaller
            q = resultcaller()
        searchstring = q
        for char in escape_chars:
            # get rid of the bullshit
            q = q.replace(char,escape_chars[char])
            
            # the old m2m did some buttfuckery on the string,
            # but for no reason that i can see, aside from historical:
            # it ran a finite automata, to differentiate between
            # quotes'd search terms and un-quots'd; as far as i can tell
            # it no longer actually used this functionality.
        
    except KeyError:
        q = ""
    

    

    # regardless, this counts as a query for stat purposes
    # but do NOT create a new row. just update the current one.
    
    latestStat = Status.objects.all().order_by("-id")[0]
    latestStat.queries += 1
    latestStat.save()
    
    
    try:
        if request.GET['optionsUp'] == "1":
            optionsUp = "1"
        else:
            optionsUp="0"
    except KeyError:
        optionsUp = "0"
    try:
        page = int(page) - 1
    except Exception:
        page = 0
    
    '''
        Declarations, extendable where possible
    '''
    paramList = [
                'type',
                'mode',
                'order',
                'useip',
                ]
    
    allowedTypes = ['none','video','audio','text','software','images',]
    allowedModes = ['dirsSubstr','filesSubstr','filesdirsSubstr',]
    allowedOrders = ['none','FileSize', '-FileSize', 'Name', '-Name',
                     'DateAdded','-DateAdded','HostName','-HostName',]
    
    ALLOWED_VALUES = {
        'type': allowedTypes,
        'mode': allowedModes,
        'order': allowedOrders,
        'useip':[1,0],
    }
    
    defaults =  {
                'type':'none',
                'mode':'filesdirsSubstr',
                'order':'none',
                'useip':0,
    }
    params = {}
    
    # fill search params, by hook or by crook
    for param in paramList: 
        try:
            if request.GET[param] in ALLOWED_VALUES[param] and request.GET[param] != "":
                # empty arguments become the default.
                params.update({param:request.GET[param]})
                
            else:
                params.update({param:defaults[param]})
        except KeyError:
            # unset params get the default too
            params.update({param:defaults[param]})
    
    
    
    # set the index and the appropriate model for later
    if params['mode']=="filesSubstr":
        indexing ='files,files-delta'
        model = File
        
    elif params['mode']=='dirsSubstr':
        indexing='directories,directories-delta'
        model = Path
    else:
        indexing='filesdirs,filesdirs-delta'
        model = File
    # type of file not specified? or searching directories
    if params['type'] == 'none' or indexing == 'directories,directories-delta':
        moding = SPH_MATCH_EXTENDED
        q2 = q
        params['type'] = 'none'
    else:
        # figure out the type
        moding = SPH_MATCH_EXTENDED2
        typeSpec = allowedTypes.index(params['type'])
        
        # type specified -> dirs are not type.
        indexing = 'files, files-delta'
        # now 'switch' through them:
        
# N.B. -- these indices are on line ~100
        # because of the way we dealt with params early on, it should always be one of
        # these, or 'none', in which case it never sees this block anyway.
        if typeSpec == 1: # video
            endings = File.videoEndings
        elif typeSpec == 2: # audio
            endings= File.audioEndings
        elif typeSpec == 3: # text
            endings = File.textEndings
        elif typeSpec == 4: #images
                endings = File.imageEndings
        else:
            endings = ""

        # The @ makes it a filter for sphinx
        q2 = q + " @filenameend ("+endings+") "
        
    # sort order
    if params['order'] == 'none':
        sorting = SPH_SORT_RELEVANCE
        sortby = ""
    else:
        sizeSpec = allowedOrders.index(params['order'])
        
        # switch through
        if sizeSpec == 1: # filesize, asc
            sorting = SPH_SORT_ATTR_ASC
            sortby = "FileSize"
        elif sizeSpec == 2: # filesize, desc
            sorting = SPH_SORT_ATTR_DESC
            sortby = "FileSize"
        elif sizeSpec == 3: # name, asc
            sorting = SPH_SORT_ATTR_ASC
            sortby = "Name"
        elif sizeSpec == 4: # name, desc
            sorting = SPH_SORT_ATTR_DESC
            sortby = "Name"
        elif sizeSpec == 5: # dateadded, asc
            sorting = SPH_SORT_ATTR_ASC
            sortby = "DateAdded"
        elif sizeSpec == 6: # dateadded, desc
            sorting = SPH_SORT_ATTR_DESC
            sortby = "DateAdded"
        elif sizeSpec == 7: #hostname, asc
            sorting = SPH_SORT_ATTR_ASC
            sortby = "HostName"
        elif sizeSpec == 8: #hostname, desc
            sorting = SPH_SORT_ATTR_ASC
            sortby = "HostName"
    if q2 == "" and sortby == "" and params['type'] == 'none':
        sorting = SPH_SORT_ATTR_DESC
        sortby = "DateAdded"
        params['order'] = '-DateAdded'
    # create client instances, filling in required attrs 
    client = SphinxClient()
    client.SetServer('labrain.st.hmc.edu',3312)
    client.SetMatchMode(moding)
    client.SetSortMode(sorting,sortby)
    # this pre-slices the results:
    client.SetLimits(page*PERPAGE,PERPAGE,maxmatches=5000)
    client.SetFilter("isdeleted",[0])
    client.SetFieldWeights({'FileName':2,'FullName':1})
    # try to search; if there's an error, escape and print the error
    try:
        result = client.Query(q2,indexing)
        while True:
            multiplier = page
            fileErrors = 0
            errorids = []
            # if no matches, no need to waste time on other things
            if result['total'] < 1:
                break
            
            resultants = result['matches']
            #populate a list with appropriate Files
            filesFound = []

            escapeLoop = False
            for fileThing in resultants:
    # N.B. -- we have to 'try' this, because sometimes the sphinx indices have
    #         records that no longer exist in the actual database.
                try:
                    filesFound += [model.objects.get(pk=fileThing['id'])]
                except:
                    # count the error hits
                    fileErrors += 1
                    errorids += [fileThing['id']]
            # something wierd happened - lots of errors
            if len(filesFound) < 1:
                multiplier += 1
                client.SetLimits(PERPAGE*multiplier,PERPAGE,maxmatches=5000)
                result = client.Query(q2, indexing)
            #got results!
            else:
                break
        try:
            filesFound
        except:
            filesFound=[]    
        if len(filesFound) > 0:
            # Substring Highlighting
            wordsToLight = []
            for entry in result['words']:
                wordsToLight += [entry['word']]
        else:
            wordsToLight = []
    # N.B -- this block will hide the highlighting, if it's after the 40th character.        
            for filerecord in filesFound:
                # as bryce says, fuck long path names with a stick:
                try:
                    filerecord.oldname = filerecord.filename
                    if len(filerecord.filename)>80:
                        filerecord.filename= filerecord.filename[0:35]+" [...] "+filerecord.filename[-40:]
                except AttributeError:
                    filerecord.oldname = filerecord.fullname
                    if len(filerecord.fullname)>80:
                        filerecord.fullname = filerecord.fullname[0:35]+" [...]"+filerecord.fullname[-40:]
                        
                        
    #----
    # for use in the template
    #----       
            # this block renders as ' PREV 1 2 3 4 5...NEXT '
        if result['total'] > PERPAGE:
            if int(page) > 6:
                paginator = range(
                        max(1,int(page)-5),# either start at 1 or 5 less than
                                               # current page
                        min(result['total']/50,int(page)+5) # go til either the
                                                                # last page or 5
                                                                # more than the 
                                                                # current one
                        )
            else:
                if result['total'] % PERPAGE > 0:
                    remainder = 1
                else:
                    remainder = 0
                paginator = range(1,min((result['total']/PERPAGE+remainder+1),11))
                    
            if page == 0 or page == 1:
                prev = 1
            else:
                prev = page - 1
            if page == max(paginator) - 1:
                    next = page
            else:
                next = page + 2
        else:
            paginator = 1
            prev = 1
            next = 1
            
        # In case no results were found, we need to set these to something
        # to avoid a NameError exception when the template loads.
        try:
            paginator
        except:
            paginator = 0
            prev = 1
            next = 1
            
    ##############################################################
    # ---- Log results of the search ---- #
    #
        # for compatibility with old shit
        logMode = {
            'none':1,
            'audio':2,
            'video':3,
            'software':4,
            'text':5,
            'images':6,
        }
        
        logType = {
            'filesSubstr':1,
            'dirsSubstr':2,
            'filesdirsSubstr':3,
        }
        # one day, this block will actually check if key exists,
        # rather than try/excepting it like a dirty migrant worker.
        try:
            client = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
         # REMOTE_ADDR is *always* 127.0.0.1
         # unless we're on test server!
            client = request.META['REMOTE_ADDR']
        newest = Log(time=time.mktime(time.localtime()),
             client=client,
             hits=result['total'],
             position=int(page)*PERPAGE,
             searchstring="Search: {}".format(q)
             mode=logType[params['mode']],
             type=logMode[params['type']],
             hosttype=3)
        newest.save()    
    ######################################################
    
        try: 
            fileErrors
        except:
            fileErrors = 0
        return render_to_response('search/results.html',
                              {
                                'title':'M2M - Results: page '+str(page+1),
                                'search':'current',
                                'q': searchstring, #so it displays all pretty-like
                                'filesfound':filesFound,
                                #'searchmeta':searchMeta,
                                'words':wordsToLight,
                                'params':params,
                                'optionsUp':optionsUp,
                                'test':test,
                                'page':int(page)+1,
                                'prev':prev,
                                'next':next,
                                'paginator':paginator,
                                'debug':DEBUG,
                                'fileErrors':fileErrors,
                                'errorids' : errorids,
                                'time': result['time'],
                                'total': result['total'],
                                'mode': params['mode'],
                                })    
    except Exception, e:
        # you should know what's up by now.
        # if not, 
        try:
            if client.GetLastError():
                error = "Query Failed: %(error)s"%{'error':client.GetLastError()}
            else:
                error = "Something went wrong; Please change your search terms! \
                        %s" % e
        except AttributeError:
            error = "Well, shit; I don't know. Probably we don't have %s" % q
        
        return render_to_response('search/results.html',
                              {
                                'title': "M2M - Resu-no, shit. What?",
                                'q':q,
                                'error':error,
                                'mode':params['mode'],
                                'optionsUp':optionsUp,
                                'page': 'WTF',
                              },)
    

def movies(request, page="q"):

    if page == "q":
        return render_to_response('base_page.html',
                                {
                                    'title':"M2M - Movies",
                                    'search':'current',
                                    'movies':'current',
                                },)
                                    

# are you in tears?
# call me, that i might bathe in them.
# 703 - 943 - 9385
