from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label='URL', max_length=1000)