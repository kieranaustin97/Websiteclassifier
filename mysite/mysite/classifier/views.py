from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import URLForm
from classifier.models import PredictedWebsites

import datetime

import classifier.scripts.website_classification as web_classifier


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():

            input_url = form.cleaned_data['url']
            classification = web_classifier.predict_site_class(input_url)
            currentDatestamp = datetime.datetime.now()
            
            context = {
                "url": input_url,
                "url_classification": classification,
                "datestamp": currentDatestamp
            }

            #Create and save output to Database
            PredictedWebsites.objects.create(
                url=input_url,
                classification=classification,
                datestamp=currentDatestamp
            )

            return render(request, 'classifier/output.html', context)
    
    else:
        form = URLForm()

    return render(request, 'classifier/home.html', {'form': form})

def showresults(request):

    previous_classification_list = PredictedWebsites.objects.all()
    context = {
        "results": previous_classification_list
    }

    return render(request, 'classifier/results.html', context)