from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import URLForm

from classifier.scripts.main import predict_site_class


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():

            input_url = form.cleaned_data['url']
            classification = predict_site_class(input_url)

            context = {
                "url": input_url,
                "url_classification": classification,
            }

            return render(request, 'classifier/output.html', context)
    
    else:
        form = URLForm()

    return render(request, 'classifier/home.html', {'form': form})

