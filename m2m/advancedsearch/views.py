from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.


def splash(request):
    
    return render_to_response('404.html')