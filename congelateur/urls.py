from django.conf.urls import patterns, url

from . import views
from congelateur.views import CongelateurListView, CongelateurDetailView, GlaceView

urlpatterns = [
    url(r'^accueil$', views.accueil, name='accueil'),
    url(r'congelateur$', CongelateurListView.as_view(), name='congo'),
    url(r'^home$', views.home, name='home'),
    url(r'^produits$',GlaceView.as_view(), name='produit'),
    url(r'^about$', views.about, name='about'),
    url(r'^discover$', views.discover, name='discover'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^produit/(?P<pk>\d+)/$', CongelateurDetailView.as_view(), name='congelo-detail'),
    url(r'^categorie/(?P<p_id>\d+)$', views.lire, name='listeCat')
]


