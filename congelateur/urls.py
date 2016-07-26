from django.conf.urls import patterns, url, include
from . import views
from congelateur.views import CongelateurListView, GlaceView, CongelateurDetailView, ClientAutocomplete

urlpatterns = [
    url(r'^accueil$', views.accueil, name='accueil'),
    url(r'congelateur$', CongelateurListView.as_view(), name='congo'),
    url(r'^home$', views.home, name='home'),
    url(r'^produits$',GlaceView.as_view(), name='produit'),
    url(r'^about$', views.about, name='about'),
    url(r'^discover$', views.discover, name='discover'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^achat/(?P<idGlace>\d+)/(?P<idClient>\d+)$', views.achat, name='achat'),
    url(r'^produit/(?P<pk>\d+)/$', CongelateurDetailView.as_view(), name='congelo-detail'),
    url(r'^categorie/(?P<p_id>\d+)$', views.lire, name='listeCat'),
    url(r'^validationAchat/(?P<idGlace>\d+)/(?P<idClient>\d+)$', views.transactionAchat, name='validationAchat'),
    url(r'^client/', include('client.urls')),
    url(r'^client-autocomplete/$', ClientAutocomplete.as_view(), name='client-autocomplete',),
    url(r'^demande/$', views.demande, name='demande'),
    url(r'^traiterDemande/(?P<idDemande>\d+)$', views.traiterDemander, name='traiterDemande'),
    url(r'^reponseDemande/(?P<demandeID>\d+)$', views.reponseDemande, name='reponseDemande'),
    url(r'^reapprovisionnement/$', views.reap, name='reap'),
    url(r'^effectuerReap/$', views.creerReap, name='creerReap'),





]


