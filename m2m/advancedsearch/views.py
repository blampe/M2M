from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.


def splash(request):
    ''' 
        An overview of the latest movies, music, and shows added to the network?
    '''
    return render_to_response('404.html')
    
def movieSplash(request):
    from models import MovieGenre,MovieCert
    
    genres = MovieGenre.objects.all()
    certs = MovieCert.objects.all()
    
    return render_to_response('advancedsearch/movies/splash.html',
        {
        'search':'current',
        'movies':'current',
        'genres': genres,
        'certs':certs,
        }
    )

def movieSearch(request, page=1):

    return render_to_response('404.html',
        {
        'search':'current',
        'movies':'current',
        }    
    )
    
def musicSplash(request):
    return render_to_response('404.html',
        {
        'search':'current',
        'music':'current',
        }
    )
    
def showSplash(request):
    return render_to_response('404.html',
        {
        'search':'current',
        'shows':'current',
        }
    )