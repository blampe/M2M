from django.shortcuts import render_to_response
from django.db.models import Sum,Min,Max

from datetime import datetime
import time as Time

from stats.models import Status, Status2, Log
from search.models import File, Host
from browseNet.models import Share,Path
# Create your views here.

def getOnlineSize():
    '''custom SQL for getting the current online size of the network'''
    from django.db import connection
    cursor = connection.cursor()
    
    cursor.execute("SELECT Sum(share.TotalFileSize) as Size FROM host LEFT JOIN share USING(hid) WHERE host.Flags & 16=16")
    
    response = cursor.fetchone()
    connection.close()
    return response

def sizeToReadable(value):
    '''takes a number of bits and reformats it to nice MB/GB/TB format'''
    try:
        value = float(value)
    except Exception:   # we expect a number, after all.
                        #or something that can be turned into a number.
        return "??"
    
    count = 0
    while value > 1024:
        value = value/1024
        count += 1
        
    if count == 1:
        appender = "KiB"
    elif count == 2:
        appender = "MiB"
    elif count == 3:
        appender = "GiB"
    elif count == 4:
        appender = "TiB"
    else:
        appender = "B"
        
    niceNum = "%.2f" % value # 1 decimal place for table formatting reasons
    
    return niceNum + " " + appender

def display(request):
    # these make the numbers small enough for google analytics urls
    BYTEDIVISOR = 1099511627776 #tsk tsk! don't use magic numbers, bryce.
    TIMEDIVISOR = 86400
    
    minSize = Status.objects.aggregate(Min('filesize'))['filesize__min']
    minSizeB = minSize/BYTEDIVISOR
    maxSize = Status.objects.aggregate(Max('filesize'))['filesize__max']
    maxSizeB = maxSize/BYTEDIVISOR
    
    minFiles = Status.objects.aggregate(Min('files'))['files__min']
    maxFiles = Status.objects.aggregate(Max('files'))['files__max']
    
    minDirs = Status.objects.aggregate(Min('directories'))['directories__min']
    maxDirs = Status.objects.aggregate(Max('directories'))['directories__max']
    
    ID = Status.objects.order_by('-id')[0].id
    #creates a unix timestamp
    maxDate = Time.mktime(datetime.now().timetuple())
    maxDateB = maxDate/TIMEDIVISOR
    
    fileSizes = ''
    numFiles = ''
    dates = ''
    dateMin = 0
    
    #begin populating the querystrings for the charts
    for counter in range(0,62):
        if ID < 1:
            break
        if counter == 0: #so we don't add a comma to the start of our strings
            delim = ""
        else:
            delim = ","
        try:
            row = Status.objects.get(pk=ID)
        except:
            break
        
        fileSizes = "%(size).2f%(delim)s%(sizes)s" % {'size':row.filesize/BYTEDIVISOR,'delim':delim,'sizes':fileSizes,}
        numFiles = "%(num)d%(delim)s%(nums)s" % {'num':row.files,'delim':delim,'nums':numFiles}
        dateMin = Time.mktime(datetime.strptime(row.lastchange,"%m/%d/%Y %H:%M").timetuple())/TIMEDIVISOR
        dates = "%(date).2f%(delim)s%(dates)s" % {'date':dateMin-maxDateB,'delim':delim,'dates':dates}
        
        ID -= 4
    
    ID = Status2.objects.aggregate(Max('id'))['id__max']-6
    
    minQ = 1000
    maxQ = 0
    
    minHosts = 1000
    maxHosts = 0
    
    queries = ''
    online = ''
    datesB = ''
    dateMinB = 0
    BADTIME = 1216103513 #whyyy bryce whyy
    for counter in range(0,98):
        if ID < 1:
            break
        if counter == 0:
            delim = ''
        else:
            delim = ','
        try:
            row0 = Status2.objects.get(pk=ID)
            row1 = Status2.objects.get(pk=ID-6)
            row2 = Status2.objects.get(pk=ID+6)
        except:
            break
        q = (row2.queries - row1.queries)/2.167 # what is this number!?
        queries = "%(q)d%(delim)s%(queries)s" % {'q':q,'delim':delim,'queries':queries}
        
        hosts = row0.onlinehosts
        if q > maxQ:
            maxQ = q
        if q < minQ:
            minQ = q
        if hosts > maxHosts:
            maxHosts = hosts
        if hosts < minHosts:
            minHosts = hosts
        
        online = "%(hosts)d%(delim)s%(online)s" % {'hosts':hosts,'delim':delim,'online':online}
        
        time = Time.mktime(row0.time.timetuple())
        if time == BADTIME:
            time -= 600 * (4056-ID)
        dateMinB = time/TIMEDIVISOR
        datesB = "%(date).2f%(delim)s%(dates)s" % {'date':dateMinB-maxDateB,'delim':delim,'dates':datesB}
        
        ID -= 11
    
    minHosts = 0 # reset this for scale purposes
    dateMin = dateMin - maxDateB
    dateMinB = dateMinB - maxDateB
    
    maxFile = 0
    maxHostSize = 0
    maxN = 10000000000000
    minN = 100
    count = minN
    fileSizesB = ''
    hostSizesB = ''
    labels = ''
    # this takes a FUCKING LONG TIME.
    # ask yourself if its worth it before you uncomment this.
    '''while count < maxN:
        count *= 100
        mini = count/100
        if count == minN:
            delim = ""
            mini = 0
        else:
            delim = ","
        
        row = len(File.objects.filter(filesize__range=(mini+1,count)))
        if row > maxFile:
            maxFile = row
        fileSizesB = "%(size)d%(delim)s%(sizes)s" % {'size':row,'delim':delim,'sizes':fileSizesB}
        
        row = len(Host.objects.filter(totalfilesize__range=(mini+1,count)))
        if row > maxHostSize:
            maxHostSize = row
        hostSizesB = "%(size)d%(delim)s%(sizes)s" % {'size':row,'delim':delim,'sizes':hostSizesB}
        labels = "%(labels)s%(delim)s%(size)s" % {'labels':labels,'delim':"|< ",'size':sizeToReadable(count)}
    
    maxFile *= 2
    '''
    
#----
#  Make the graph queries themselves
#----
   


    querySrc = "http://chart.apis.google.com/chart?\
               cht=lxy&\
               chd=t:%(datesB)s|%(online)s|%(datesB)s|%(queries)s&\
               chds=%(dateMinB)f,0,0,%(maxQ)d,%(dateMinB)f,0,0,%(maxQ)d&\
               chdl=Online Hosts|Queries/Hr&\
               chco=ABD1E6,000000&\
               chxt=x,y,x,r&\
               chxl=2:||Days|&\
               chxr=0,%(dateMinB)f,0|1,0,%(maxQ)d|3,0,%(maxQ)d&\
               chs=380x200" % {
        'datesB':datesB,
        'online':online,
        'queries':queries,
        'dateMinB':dateMinB,
        'minHosts':minHosts,
        'maxHosts':maxHosts,
        'maxQ':maxQ,
        'minQ':minQ,
    }
    
    sizeSrc = "http://chart.apis.google.com/chart?\
              cht=lxy&\
              chd=t:%(dates)s|%(numFiles)s|%(dates)s|%(fileSizes)s&\
              chds=%(dateMin)f,0,%(minFiles)d,%(maxFiles)d,%(dateMin)f,0,%(minSizeB)d,%(maxSizeB)d&\
              chdl=Files|Total Size (TiB)&\
              chco=ABD1E6,000000&\
              chxt=x,y,x,r&\
              chxl=2:||Days|&\
              chxr=0,%(dateMin)f,0|1,%(minSizeB)d,%(maxSizeB)d|3,%(minFiles)d,%(maxFiles)d&\
              chdlp=r&\
              chs=440x200" % {
        'dates':dates,
        'numFiles':numFiles,
        'fileSizes':fileSizes,
        'minFiles':minFiles,
        'maxFiles':maxFiles,
        'dateMin':dateMin,
        'minSizeB':minSizeB,
        'maxSizeB':maxSizeB,
    }
    
   # if len(sizeSrc) > 2048:
    #    sizeSrc = "http://chart.apis.google.com/chart?chs=440x200&chf=bg,s,ffffff&cht=t&chtm=world&chco=ecf3fe,cccccc,0000ff&chld=US&chd=t:100"
    
    barsizeSrc = "http://chart.apis.google.com/chart?cht=bvs&\
                 chco=000000,ABD1E6&\
                 chs=820x50&chbh=a&\
                 chxt=x,y,r&\
                 chdl=Files|Hosts&chxl=0:%(labels)s|&\
                 chxr=1,0,%(maxFile)d|2,0,%(maxHostSize)d&\
                 chds=0,%(maxFile)d,0,%(maxHostSize)d&\
                 chd=t:%(fileSizesB)s|%(hostSizesB)s" %{
        'labels':labels,
        'maxFile':maxFile,
        'maxHostSize':maxHostSize,
        'fileSizesB':fileSizesB,
        'hostSizesB':hostSizesB,
    }



#----
# And now for the cold, hard numbers
#----
    
    infoHolder = Status.objects.all().order_by('-id')[0]
    lastCrawl = infoHolder.lastchange
    indexedServers = infoHolder.smbhosts
    dirCount = infoHolder.directories
    fileCount = infoHolder.files
    netSize = sizeToReadable(infoHolder.filesize)
    queryCount = infoHolder.queries
    
    infoHolder = Status2.objects.all().order_by('-id')[0]
    onlineServers = infoHolder.onlinehosts
    
    onlineSize = sizeToReadable(getOnlineSize()[0])
    
#----
# Pulling info from the Log table
#----
    '''
    # Last activity:
    latestActivity = Log.objects.raw("SELECT * FROM log ORDER BY LID DESC LIMIT 5")
    latestActions = []
    for row in latestActivity:
        action = row.searchstring.split()
        
        actions = [
            'browse',
            'Browse:',
            'Search:',
        ]
        
        if action[0] in actions:
            # BROWSE
            if action[0] == actions[0] or action[0] == actions[1]:
                
                #now, parse the browse.
                
                #action[1] should be in the form "HID=?,PID=?,SID=?"
                if action[0] == actions[0]:
                    pieces = action[1].split(',')
                    taped = []
                    for piece in pieces:
                        taped += [piece.split('=')]
                    
                    if taped[0][1] != '0': # HOST
                        host = Host.objects.get(pk=int(taped[0][1]))
                        
                    elif taped[1][1] != '0': # SHARE
                        host = Share.objects.get(pk=int(taped[1][1])).hostid
                        
                    elif taped[2][1] != '0': # PATH
                        host = Path.objects.get(pk=int(taped[2][1])).hid
                    
                    else:
                        host = "??"
                #action[1:] should be in the form ["H/S/P,","####"]
                elif action[0] == actions[1]:
                    if action[1] == "H,":
                        host = Host.objects.get(pk=int(action[2]))
                        
                    elif action[1] == "S,":
                        host = Share.objects.get(pk=int(action[2]))
                    
                    elif action[1] == "P,":
                        host = Path.objects.get(pk=int(action[2]))
                    
                    else:
                        host = "??"
                else:
                    host = "??"
                        
                
                lastAction = "%(ip)s browsed %(host)s" % {'ip':row.client,'host':host}
        
        # a search from new M2M
            elif action[0] == actions[2]:
                lastAction = "%(ip)s searched for %(search)s" % {'ip':row.client,'search':''.join(action[1:])}
            
        # a search from old M2M
        else:
            lastAction ="%(ip)s searched for %(search)s" % {'ip':row.client,'search':" ".join(action)}
            
        latestActions += [lastAction]
    '''
    debug = {
                               'querySrc':querySrc,
                               'sizeSrc':sizeSrc,
                               'barsizeSrc':barsizeSrc,
                               'lastCrawl':lastCrawl,
                               'indexedServers':indexedServers,
                               'onlineServers':onlineServers,
                               'dirCount':dirCount,
                               'fileCount':fileCount,
                               'netSize':netSize,
                               'onlineSize':onlineSize,
                               'queryCount':queryCount,
                              }
    
    return render_to_response("stats/display.html",
                              {
                               'stats':'current',
                               'siteStat':'current',
                               'querySrc':querySrc,
                               'sizeSrc':sizeSrc,
                               'barsizeSrc':barsizeSrc,
                               'lastCrawl':lastCrawl,
                               'indexedServers':indexedServers,
                               'onlineServers':onlineServers,
                               'dirCount':dirCount,
                               'fileCount':fileCount,
                               'netSize':netSize,
                               'onlineSize':onlineSize,
                               'queryCount':queryCount,
                               #'lastActions':latestActions,
                               'debug':debug,
                              },)