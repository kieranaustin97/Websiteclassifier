"""Django Views File"""
import re
import datetime
import requests

from classifier.models import PredictedWebsites
import classifier.scripts.website_classification as web_classifier

from django.shortcuts import render
from .forms import URLForm

# Create your views here.
def index(request):
    """Main index view for webpage"""
    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():

            current_datestamp = datetime.datetime.now()
            input_url = form.cleaned_data['url']
            method_check = re.search('^http://|^https://',input_url)
            if method_check:
                url = input_url
            else:
                url = "http://" + input_url
            try:
                url, classification = web_classifier.predict_site_class(url)
            except requests.exceptions.Timeout:
                context = {
                    "url": url,
                    "url_classification": "HTML Currently Unavilable and therefore no Classification provided",
                    "datestamp": current_datestamp,
                    "colour":"Red"
                }
                return render(request, 'classifier/output.html', context)
            except requests.exceptions.ConnectionError:
                context = {
                    "url": input_url,
                    "url_classification": "HTML Currently Unavilable and therefore no Classification provided",
                    "datestamp": current_datestamp,
                    "colour":"Red"
                }
                return render(request, 'classifier/output.html', context)
            else:
                context = {
                    "url": url,
                    "url_classification": classification,
                    "datestamp": current_datestamp,
                    "colour":"black"
                }
                #Create and save output to Database
                PredictedWebsites.objects.create(url=url,classification=classification,datestamp=current_datestamp)
                return render(request, 'classifier/output.html', context)

    else:
        form = URLForm()
        context = {
            'class_array':web_classifier.list_possible_classes(),
            'form':form
        }
        return render(request, 'classifier/home.html', context)

def showresults(request):
    """Showresults view for displaying all previous classifications on frontend"""
    #Deletes item from table if delete form submitted
    if request.method == "POST":
        PredictedWebsites.objects.get(id=request.POST['id']).delete()
    
    #Collects all objects from database
    previous_classification_list = PredictedWebsites.objects.all()

    #Check if any objects retrieved, if there is none return blank page instead of table
    if len(previous_classification_list) == 0:
        return render(request, 'classifier/noResults.html')
    
    context = {"results": previous_classification_list}
    return render(request, 'classifier/results.html', context)
