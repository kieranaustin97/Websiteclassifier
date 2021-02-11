from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import URLForm
from classifier.models import PredictedWebsites
import classifier.scripts.website_classification as web_classifier

import datetime

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
    #Deletes item from table if delete form submitted
    if request.method == "POST":
        PredictedWebsites.objects.get(id=request.POST['id']).delete()
    
    #Collects all objects from database
    previous_classification_list = PredictedWebsites.objects.all()

    #Check if any objects retrieved, if there is none return blank page instead of table
    if len(previous_classification_list) == 0:
        return render(request, 'classifier/noResults.html')

    else:
        context = {
            "results": previous_classification_list
        }
        return render(request, 'classifier/results.html', context)