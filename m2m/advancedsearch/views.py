from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count

from datetime import datetime
import time

from stats.models import Status, Log
from models import MovieGenre,MovieCert,Movie,\
                    MusicGenre,Artist,Song,Album
# Create your views here.

PERPAGE_MOV = 50
PERPAGE_MUS = 20
PERPAGE_MUS_SONG = 50
PERPAGE_SHO = 50

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
def splash(request):
    ''' 
        An overview of the latest movies, music, and shows added to the network?
    '''
    return render_to_response('404.html')
    
def movieSplash(request):
    import random
    
    genres = MovieGenre.objects.all()
    certs = MovieCert.objects.all()
    
    # filter by date, don't show movies without files
    latestMovies = list(Movie.objects.order_by('-dateadded').annotate(num_files=Count('files')).filter(num_files__gte=1)[:12])
    
    random.shuffle(latestMovies)
    
    return render_to_response('advancedsearch/movies/splash.html',
        {
        'search':'current',
        'movies':'current',
        'genres': genres,
        'certs':certs,
        'latestMovies':latestMovies,
        }
    )

def movieRandom(request):
    
    movieId = Movie.objects.order_by('?')[:1][0].id
    
##############################################################
# ---- Log results of the search ---- #
#
    try:
        client = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
     # REMOTE_ADDR is *always* 127.0.0.1, but the above doesn't work
     # on test boxes using the django server
        client = request.META['REMOTE_ADDR']
        
    newest = Log(time=time.mktime(time.localtime()),
                 client=client,
                 hits=p.count,
                 position=page*PERPAGE_MOV,
                 searchstring="Search [MOVIE - RANDOM]")
    newest.save()
######################################################
    
    return movieDetail(request,movieId)
    
    
def movieSearch(request, page=1):
    from django.core.paginator import Paginator
    
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
        page = int(page) - 1 if int(page) > 1 else 0
    except Exception:
        page = 0
    
    paramList = [
                'genre',
                'cert',
                'order',
                ]
    # list comprehensions for the winnnn
    genres = [x.name for x in MovieGenre.objects.all()]
    certs = [x.cert for x in MovieCert.objects.all()]
    
    allowedOrders = ['none',
            'name', '-name',
            'dateadded','-dateadded',
            'rating','-rating',
            'popularity','-popularity',
            'runtime','-runtime']
    
    ALLOWED_VALUES = {
        'genre':genres,
        'cert':certs,
        'order':allowedOrders,
    }
    
    defaults = {
        'genre':'all',
        'cert':'all',
        'order':'none',
    }
    params = {}
    
    # fill in params from GET
    for param in paramList:
        try:
            if request.GET[param] in ALLOWED_VALUES[param] and request.GET[param] != "":
                params.update({param:request.GET[param]})
                
            else:
                params.update({param:defaults[param]})
        except KeyError:
            # some options weren't chosen - we set them here.
            params.update({param:defaults[param]})
            
    # don't search movies without files - these will get cleared out of database later
    movieList = Movie.objects.all().annotate(num_files=Count('files')).filter(num_files__gte=1)
    
    if q != "":
        movieList = movieList.filter(name__icontains=q)
    
    if params['genre'] != 'all':
        movieList = movieList.filter(genres__name=params['genre'])
    
    if params['cert'] != 'all':
        movieList = movieList.filter(cert__cert=params['cert'])
    
    if params['order'] != 'none':
        movieList = movieList.order_by(params['order'],params['order'] if params['order'][0] != '-' else params['order'][1:])
    
    try:
        optionsUp = '1' if request.GET['optionsUp'] == '1' else '0'
    except KeyError:
        optionsUp='0'
    p = Paginator(movieList,PERPAGE_MOV)
    
##############################################################
# ---- Log results of the search ---- #
#
    try:
        client = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
     # REMOTE_ADDR is *always* 127.0.0.1
     # unless we're on test server!
        client = request.META['REMOTE_ADDR']
        
    newest = Log(time=time.mktime(time.localtime()),
                 client=client,
                 hits=p.count,
                 position=page*PERPAGE_MOV,
                 searchstring=u"Search [MOVIE]: {}".format(q))
    newest.save()
######################################################
    
    return render_to_response('advancedsearch/movies/results.html',
        {
        'search':'current',
        'movies':'current',
        'genres':MovieGenre.objects.all(),
        'certs':MovieCert.objects.all(),
        'optionsUp':optionsUp,
        'q':q,
        'object_list':p.page(page+1).object_list,
        'page':p.page(page+1),
        'paginator':p,
        'params':params,
        
        }    
    )
    
def movieDetail(request,id):
    from models import Movie

    movie = get_object_or_404(Movie,pk=id)
    
    return render_to_response('advancedsearch/movies/detail.html',
        {'movie':movie,
          'movies':'current',
          'search':'current',})
    
def musicSplash(request):
    import random
    latestAlbums = list(Album.objects.all().order_by('-dateadded')[:48])
    random.shuffle(latestAlbums)
    
    return render_to_response('advancedsearch/music/splash.html',
        {
        'search':'current',
        'music':'current',
        'genres':MusicGenre.objects.all(),
        'latest':latestAlbums,
        }
    )

def musicBrowse(request,page=0):
    from django.core.paginator import Paginator
    try:
        page = int(page) - 1 if int(page) > 1 else 0
    except Exception:
        page = 0
    artists = Artist.objects.all().order_by('name')
    
    p = Paginator(artists,PERPAGE_MUS)
    return render_to_response('advancedsearch/music/browse.html',
    {
    'search':'current',
    'music':'current',
    'genres':MusicGenre.objects.all(),
    'p':p,
    'object_list':p.page(page+1).object_list,
    'page':p.page(page+1),
    })
    
    
    
def musicSearch(request):  
    ''' Wrapper for the more detailed searching required by the nature
        of music searching. '''
##############################################################
# ---- Log results of the search ---- #
#
    try:
        client = request.META['HTTP_X_FORWARDED_FOR']
    except KeyError:
     # REMOTE_ADDR is *always* 127.0.0.1
     # unless we're on test server!
        client = request.META['REMOTE_ADDR']
        
    newest = Log(time=time.mktime(time.localtime()),
                 client=client,
                 searchstring=u"Search [MUSIC]: {}".format(request.GET['q']))
    newest.save()
######################################################    
        
    # hand these off to helper methods - which we have so that you can
    # page through each set of results individually, via AJAX
    #songset = musicSearch_Song(q)
    #albumset = musicSearch_album(q)
    #artistset = musicSearch_artist(q)
    paramList = [
                'genre',
                'order',
                'type',
                ]   
    genres = [x.name for x in MusicGenre.objects.all()]
    
    allowedTypes = ['Song','Album','Artist']
    
    allowedOrders = ['none',
            'name', '-name',
            'dateadded','-dateadded',
            'rating','-rating',
            'popularity','-popularity',
            'runtime','-runtime']
    
    ALLOWED_VALUES = {
        'genre':genres,
        'order':allowedOrders,
        'type':allowedTypes,
    }
    
    defaults = {
        'genre':'all',
        'order':'none',
        'type':'all',
    }
    params = {}
    
    # fill in params from GET
    for param in paramList:
        try:
            if request.GET[param] in ALLOWED_VALUES[param] and request.GET[param] != "":
                params.update({param:request.GET[param]})
                
            else:
                params.update({param:defaults[param]})
        except KeyError:
            # some options weren't chosen - we set them here.
            params.update({param:defaults[param]})    
    
    
    try:
        optionsUp = '1' if request.GET['optionsUp'] == '1' else '0'
    except KeyError:
        optionsUp='0'
    
    return render_to_response('advancedsearch/music/results.html',
        {
        'search':'current',
        'music':'current',
        'genres':MusicGenre.objects.all(),
        'q':request.GET['q'],
        'params':params,
        'optionsUp':optionsUp,
        }
    )
    
def musicSearch_Song(request=None,page=0):
    from django.core.paginator import Paginator
    
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
        
    except KeyError:
        q = ""
    
    try:
        page = int(page) - 1 if int(page) > 1 else 0
    except Exception:
        page = 0
    
    songset = Song.objects.filter(name__icontains=q)
    
    p = Paginator(songset,PERPAGE_MUS_SONG)    
    return render_to_response('advancedsearch/music/subresults.html',
        {'p':p,
         'q':q,
         'type':'Song',
         'object_list':p.page(page+1).object_list,
         'page':p.page(page+1),
         }
    )
    
def musicSearch_Album(request=None, q='',page=0):
    from django.core.paginator import Paginator
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
        
    except KeyError:
        q = ""
    
    try:
        page = int(page) - 1 if int(page) > 1 else 0
    except Exception:
        page = 0
        
    albumset = Album.objects.filter(name__icontains=q)
    
    p = Paginator(albumset,PERPAGE_MUS)
    return render_to_response('advancedsearch/music/subresults.html',
        {'p':p,
         'q':q,
         'type':'Album',
         'object_list':p.page(page+1).object_list,
         'page':p.page(page+1),}
    )
    
def musicSearch_Artist(request=None, q='',page=0):
    from django.core.paginator import Paginator
    
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
        
    except KeyError:
        q = ""
    
    try:
        page = int(page) - 1 if int(page) > 1 else 0
    except Exception:
        page = 0
    
    artistset = Artist.objects.filter(name__icontains=q)

    p = Paginator(artistset,PERPAGE_MUS)            
    return render_to_response('advancedsearch/music/subresults.html',
        {'p':p,
         'q':q,
         'type':'Artist',
         'object_list':p.page(page+1).object_list,
         'page':p.page(page+1),
        }
    )
    
def artistDetail(request,id="Q"):

    artist = get_object_or_404(Artist,pk=id)

    return render_to_response('advancedsearch/music/artistDetail.html',
        {
        'search':'current',
        'music':'current',
        'artist':artist,
        }
    )

def albumDetail(request,id="Q"):
    album = get_object_or_404(Album,pk=id)

    return artistDetail(request,album.artist.id)
    '''
    return render_to_response('404.html',
        {
        'search':'current',
        'shows':'current',
        }
    )
    '''
def songDetail(request,id="Q"):
    return render_to_response('404.html',
        {
        'search':'current',
        'shows':'current',
        }
    )
    
def showSplash(request):
    return render_to_response('404.html',
        {
        'search':'current',
        'shows':'current',
        }
    )