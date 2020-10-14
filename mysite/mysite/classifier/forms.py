from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label='url', max_length=1000)