from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.


def sitewide(request):
    
    message = "We're in the middle of migrating to some new technologies.\n\
              Please bear with us; normal service should begin momentarily."
    
    return general(request,message)
    
def requests(request):
    
    return general(request)
    

def stats(request):
    
    message = " The stats page is under some heavy, heavy construction. You may\
              have noticed that it's been gone for a while now. \
              Maybe you haven't; let me tell you now: it has. It's a complicated\
              page, and alot of its old methods didn't translate very well to\
              our new set up, so it might be a little while before this is back\
              up and running."
    
    return general(request,message)
    
def browseNet(request):
    
    return general(request)
    
def polls(request):
    
    message = "The polls page will allow you to ask questions of your fellow students,\
              and servers to connect with users more directly than ever before. It will\
              allow prioritizing of downloads, and all that good stuff. \n Get excited!"
    
    return construction(request,message)
    
def news(request):
    
    return general(request)
    
def general(request,message=''):
    
    return render_to_response('problems/general.html',
                              {
                                'message':message,
                                })

def construction(request,message=''):
    
    return render_to_response("problems/construction.html",
                              {
                                'message':message,
                              })
                              
def host(request,id):
    from browseNet.models import Host
    
    host = get_object_or_404(Host, pk=id)
    try:
        problems = host.problems
    except:
        from browseNet.views import listAll
        return listAll(request)

    return render_to_response("problems/host.html",
                                {
                                'host':host,
                                'pset':problems,
                                'servers':'current'
                                })
