from django import forms
from m2m.requests.models import Comment

class RequestForm(forms.Form):
    error_css_class='error'
    required_css_class = 'required'
    
    request = forms.CharField(widget=forms.Textarea(attrs={'rows':'9','cols':'50'}),required=True)
    name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Anonymous'}),required=False)
    server = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'i.e. M2M','title':'Please, no \'\\\\\' here.',}),required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'your_name@hmc.edu','title':'You\'ll get an email when the request is completed.'}),required=False)
    
        
class ModifyForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class='required'
    
    # EDIT fields
    request = forms.CharField(widget=forms.Textarea(attrs={'rows':'9','cols':'50'}),required=True)
    server = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'i.e. M2M','title':'Please, no \'\\\\\' here.',}),required=False)
    
    # COMPLETE fields
    completerComment = forms.CharField(widget=forms.Textarea(attrs={'rows':'9','cols':'50'}),required=False)
    completingServer = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'M2M','title':'Please, no \'\\\\\' here.',}),required=True)
    class Meta:
        model = Comment
        # we do not want this shiiiit
        exclude = ('requestTime','completed','completedTime','isDeleted','Likes',)


class EditForm(ModifyForm):

    request = forms.CharField(widget=forms.Textarea(attrs={'rows':'9','cols':'50'}),required=True)
    server = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'i.e. M2M','title':'Please, no \'\\\\\' here.',}),required=False)
    
    class Meta:
        exclude = True
        #exclude += ('completingServer','completerComment',)

class CompleteForm(ModifyForm):

    completerComment = forms.CharField(widget=forms.Textarea(attrs={'rows':'9','cols':'50'}),required=False)
    completingServer = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'M2M','title':'Please, no \'\\\\\' here.',}),required=True)

    class Meta:
        exclude = True
        #exclude += ('email','name','server','request',)
