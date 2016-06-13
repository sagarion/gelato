from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from congelateur.models import Glace, Congelateur, Categorie
from transaction.models import Transaction, LigneTransaction
from client.models import *
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from django.contrib import messages

# Create your views here.


def accueil(request):
    return render(request, 'congelateur/accueil.html', locals())

def about(request):
    return render(request, 'congelateur/about.html')

def discover(request):
    return render(request, 'congelateur/discover.html', locals())

@login_required
def dashboard(request):
    return render(request, 'congelateur/dashboard.html', locals())

def home(request):
    return render(request, 'congelateur/home.html')

@login_required
def achat(request, idGlace, idClient):
    cli = get_object_or_404(User, id=idClient)
    compte = get_object_or_404(Compte, user=idClient)
    solde = compte.solde
    glace = get_object_or_404(Glace, id=idGlace)

    if(glace.prixVente > solde):
        messages.error(request, 'Solde insuffisant !')
        #return render(request, 'congelateur/glace_list.html')
        return redirect('produit')
    else:
        return render(request, 'congelateur/achat.html', {'gl': glace})


class GlaceView(TemplateView):
    template_name = 'congelateur/glace_list.html'

    def get_context_data(self, **kwargs):
        context = super(GlaceView, self).get_context_data(**kwargs)

        context['glaces'] = Glace.objects.filter(statut='A')
        #context['glaces'] = Glace.objects.all()
        #Post.objects.filter(author=me)
        context['cats'] = Categorie.objects.all()
        return context


def lire(request, p_id):
    categorie = get_object_or_404(Categorie, id=p_id)
    glaces = []

    if categorie.sousCategorie is None:

        lesCat = Categorie.objects.filter(sousCategorie=categorie.id)

        for p in lesCat:
            pk = p.id
            uneCat = Glace.objects.filter(cat=pk)
            for u in uneCat:
                glaces.append(u)
    else:
        glaces = Glace.objects.filter(cat=p_id)

    toutesLesCats = Categorie.objects.all()

    return render(request, 'congelateur/glace_categorie.html', {'cat': categorie, 'gl': glaces, 'cats':toutesLesCats})



class CongelateurListView(ListView):
    queryset = Congelateur.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super(CongelateurListView, self).get_context_data(**kwargs)
        return context

class CongelateurDetailView(DetailView):
    model = Congelateur
    def get_context_data(self, **kwargs):
        context = super(CongelateurDetailView, self).get_context_data(**kwargs)
        return context


def transactionAchat(request, idGlace, idClient):
    cli = get_object_or_404(User, id=idClient)
    glace = get_object_or_404(Glace, id=idGlace)
    compte = get_object_or_404(Compte, user=idClient)
    solde = compte.solde

    bac = glace.bac
    tiroir = bac.tiroir
    congo = tiroir.congelateur

    t = Transaction()
    t.type = 'A'
    t.code = timezone.now()
    t.client = cli
    t.total = 0
    t.save()


    ligne = LigneTransaction()
    ligne.transaction = t
    ligne.glace = glace
    ligne.quantite = 1
    ligne.prix = glace.prixVente
    t.total = t.total + ligne.prix
    glace.statut = 'V'

    compte.solde = solde - t.total

    compte.save()
    glace.save()
    ligne.save()
    t.save()

    return render(request, 'congelateur/RecapAchat.html', {'bac': bac, 'tiroir':tiroir, 'congo':congo, 'solde':compte.solde})

