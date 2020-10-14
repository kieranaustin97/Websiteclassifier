from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import URLForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    
    else:
        form = URLForm()

    return render(request, 'classifier/home.html', {'form': form})
