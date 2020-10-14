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
            print(input_url)
            classification = predict_site_class(input_url)
            print("CLASSSSSSSSSSSSSSS" + classification)
            #test_output = subprocess.run('python mysite/mysite/classifier/scripts/test_script.py', stdout=PIPE, encoding='utf-8')

            #print(test_output.stdout)
            
            return HttpResponseRedirect('/thanks/')
    
    else:
        form = URLForm()

    return render(request, 'classifier/home.html', {'form': form})
