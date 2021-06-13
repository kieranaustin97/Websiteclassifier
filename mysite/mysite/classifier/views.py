"""Django Views File"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import classifier
import re
from django.utils import timezone
import requests

from classifier.models import PredictedWebsites
#import classifier.scripts.website_classification as web_classifier
from classifier.scripts.website_classification import WebsiteClassification
from django.shortcuts import redirect, render
from .forms import URLForm

WebsiteClassifier = WebsiteClassification()

# Create your views here.
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {
                "error": "Username or Password Incorrect"
            }

    return render(request, 'classifier/login.html', context)

def logOut(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    """Main index view for webpage"""
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            current_datestamp = timezone.now()
            input_url = form.cleaned_data['url']
            method_check = re.search('^http://|^https://',input_url)
            if method_check:
                url = input_url
            else:
                url = "http://" + input_url
            try:
                url, classification = WebsiteClassifier.predict_site_class(url)
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
            'class_array':WebsiteClassifier.list_possible_classes(),
            'form':form
        }
        return render(request, 'classifier/home.html', context)

@login_required(login_url='login')
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
