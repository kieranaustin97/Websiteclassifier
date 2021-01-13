from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import URLForm
from classifier.models import PredictedWebsites

#Import Machine Learning classification function from website_classification.py file
from classifier.scripts.website_classification import predict_site_class

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

            #Create and save output to Database
            PredictedWebsites.objects.create(
                url=input_url,
                classification=classification
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