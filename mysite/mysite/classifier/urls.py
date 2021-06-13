"""Django URL File"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'showresults', views.showresults, name='showresults'),

    url(r'login',views.loginPage, name='login'),
    url(r'logout',views.logOut, name='logout')
    ]
