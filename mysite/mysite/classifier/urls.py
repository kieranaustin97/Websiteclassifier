"""Django URL File"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'showresults', views.showresults, name='showresults')
]
