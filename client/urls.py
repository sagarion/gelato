from django.conf.urls import patterns, url
from . import views

from . import views

urlpatterns = [

url(r'^connexion$', views.connexion, name='connexion'),
url(r'^deconnexion$', views.deconnexion, name='deconnexion'),


]


