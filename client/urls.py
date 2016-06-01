from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

url(r'^connexion$', views.connexion, name='connexion'),
url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
url(r'^connexion$', auth_views.login, {'template_name': 'auth/connexion.html'})


]


