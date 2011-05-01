from django.shortcuts import render_to_response
from django.template import RequestContext

from django import forms


# Create your views here.

class FAQForm(forms.Form):
	error_css_class='error'
	required_css_class = 'required'
	
	question = forms.CharField(widget=forms.Textarea(attrs={
					'rows':'9',
					'cols':'50',
					'placeholder':'Why are you so handsome, M2M?'
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
		form = FAQForm()
	
	return render_to_response('faq/server.html',
								{
								'title': 'M2M - FAQ:Servers',
								'faq':'current',
								'server':'current',
								'section':'servers',
								'form': form,
								},context_instance=RequestContext(request))