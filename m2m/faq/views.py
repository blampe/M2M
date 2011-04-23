from django.shortcuts import render_to_response
# Create your views here.

def basic(request):
    ''' displays the generic faq, without any specialization '''
    
    return render_to_response('faq/basic.html',
								{
								'title': 'M2M - FAQ',
								'faq': 'current',
								'basic':'current',
								})
							  
def servers(request):
	''' displays the server-specific faq'''
	return render_to_response('faq/server.html',
								{
								'title': 'M2M - FAQ:Servers',
								'faq':'current',
								'server':'current',
								})