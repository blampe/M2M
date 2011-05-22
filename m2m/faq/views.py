from django.shortcuts import render_to_response
from django.template import RequestContext

from django import forms

import random

# Create your views here.

class FAQForm(forms.Form):
    error_css_class='error'
    required_css_class = 'required'
    
    # just for fun, placeholder questions
    questions = ['I swear to god, if you spam me...']*5
    questions += ['Why are you so handsome, M2M?', 
                'Who\'s your daddy?', 
                'How *you* doin\'?',
                'Anyone for tea?',
                'Fezzes are cool.',
                'Are you sure about that?',
                ]
    
    def __init__(self):
        super(FAQForm,self).__init__()
        
        self.fields['question'] = forms.CharField(widget=forms.Textarea(attrs={
                    'rows':'9',
                    'cols':'50',
                    'placeholder':random.choice(self.questions),
                    }),required=True)
        
    

def basic(request):
    ''' displays the generic faq, without any specialization '''
    
    if request.method == 'POST':
        from django.core.mail import send_mail
        recipients = ['haak.erling@gmail.com',]
        # No matter what, we should have a form.
        form = FAQForm(request.POST)
        if form.is_valid():
            # Set the appropriate subject lines...
            subject = "FAQ - Basic"
            q = form.cleaned_data['question']
            send_mail(subject,q,'faq@m2m.st.hmc.edu',recipients)
    else:
        form = FAQForm()
        
    return render_to_response('faq/basic.html',
                                {
                                'title': 'M2M - FAQ',
                                'faq': 'current',
                                'basic':'current',
                                'section':'basic',
                                'form' : form,
                                },context_instance=RequestContext(request))
                              
def servers(request):
    ''' displays the server-specific faq'''
    
    # This is stupid, duplicated code, but django is a big bitch about 
    # dedicated POST-processing views.
    
    if request.method == 'POST':
        from django.core.mail import send_mail
        recipients = ['haak.erling@gmail.com',]
        # No matter what, we should have a form.
        form = FAQForm(request.POST)
        if form.is_valid():
            # Set the appropriate subject lines...
            subject = "FAQ - Servers"
            q = form.cleaned_data['question']
            send_mail(subject,q,'faq@m2m.st.hmc.edu',recipients)
    else:
        random.seed()
    form = FAQForm()
    
    return render_to_response('faq/server.html',
                                {
                                'title': 'M2M - FAQ:Servers',
                                'faq':'current',
                                'server':'current',
                                'section':'servers',
                                'form': form,
                                },context_instance=RequestContext(request))
                                
def about(request,typeof='m2m'):
    ''' handles the about pages. This seemed like a good place to put them.'''
    if typeof == 'm2m':
        return render_to_response('faq/m2m.html',
                                {
                                'title': 'M2M - About: M2M',
                                'about':'current',
                                'section':'about',

                                },context_instance=RequestContext(request))
    
    return render_to_response('faq/basic.html',
                                {
                                'title': 'M2M - About: M2M',
                                'faq':'current',
                                'section':'about',

                                },context_instance=RequestContext(request))
                                

def serviceTerms(request):

    return render_to_response('faq/tos.html',
                            {'title':'M2M - Terms of Service'},
                            )
                            
def dmca(request):
    return render_to_response('404.html')
    
def privacy(request):

    return render_to_response('404.html')