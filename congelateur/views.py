import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from congelateur.models import *
from transaction.models import Transaction, LigneTransaction
from client.models import *
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from django.contrib import messages
from dal import autocomplete
from .forms import *
from django.db.models import Q
from decimal import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def accueil(request):
    return render(request, 'congelateur/accueil.html', locals())

def about(request):
    return render(request, 'congelateur/about.html')

def discover(request):
    return render(request, 'congelateur/discover.html', locals())


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Compte.objects.none()

        qs = Compte.objects.all()

        if self.q:
            qs = qs.filter(nom__startswith=self.q)

        return qs


@login_required
def dashboard(request):
    userConnected = request.user
    compte = get_object_or_404(Compte, user=userConnected)
    listeUtilisateurs = Compte.objects.exclude(user=userConnected)
    list_transactions = Transaction.objects.filter(client=compte).order_by('-date')
    #Toutes les demandes :
    # transferts = Demande.objects.filter(Q(clientDemandeur=compte) | Q(clientReceveur=compte))
    demandesFaites = Demande.objects.filter(clientDemandeur=compte)
    demandesRecues = Demande.objects.filter(clientReceveur=compte)
    demandesATraiter = Demande.objects.filter(Q(clientReceveur=compte) & Q(etat='En attente'))
    modes = Mode.objects.all()
    form = DemandeForm()

    #Pagination pour les transactions
    paginator = Paginator(list_transactions, 5)

    page = request.GET.get('page')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        transactions = paginator.page(paginator.num_pages)




    return render(request, 'congelateur/dashboard.html', {'user':compte, 'listUsers':listeUtilisateurs, 'transactions':transactions,
                                                          'mode':modes, 'form': form, 'demandesFaites':demandesFaites, 'demandesRecues':demandesRecues, 'demandeATraiter':demandesATraiter})


def demande(request):
    userConnected = request.user
    compte = get_object_or_404(Compte, user=userConnected)
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = DemandeForm(request.POST)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            # Ici nous pouvons traiter les données du formulaire
            montant = form.cleaned_data['montant']
            mode = form.cleaned_data['mode']
            #dateReponse = form.cleaned_data['dateReponse']
            #accepte = form.cleaned_data['accepte']
            clientDemandeur = userConnected
            clientReceveur = form.cleaned_data['clientReceveur']
            if clientReceveur.solde < montant :
                messages.info(request, 'Le solde du client n\'est pas suffisant !')
            else :

                d = Demande()
                d.montant = montant
                d.mode = mode
                d.clientDemandeur = compte
                d.clientReceveur = clientReceveur
                d.etat = 'En attente'

                d.save()
                """send_mail(
                    'Subject here',
                    'Here is the message.',
                    'schaffner20@gmail.com',
                    ['schaffner.colin@bluewin.ch.com'],
                    fail_silently=False,
                )"""

                messages.info(request, 'Demande envoyée !')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = DemandeForm()  # Nous créons un formulaire vide

    return dashboard(request)

def home(request):
    return render(request, 'congelateur/home.html')

@login_required
def achat(request, idGlace, idClient):
    cli = get_object_or_404(User, id=idClient)
    compte = get_object_or_404(Compte, user=idClient)
    solde = compte.solde
    glace = get_object_or_404(Produit, id=idGlace)
    soldeApresAchat = solde - glace.prixVente

    if(glace.prixVente > solde):
        messages.error(request, 'Solde insuffisant !')
        return redirect('produit')
    else:
        return render(request, 'congelateur/achat.html', {'gl': glace, 'soldeSiAchat':soldeApresAchat})


class GlaceView(TemplateView):
    template_name = 'congelateur/glace_list.html'

    def get_context_data(self, **kwargs):
        context = super(GlaceView, self).get_context_data(**kwargs)

        #Plus grand que se traduit par : __gt
        context['glaces'] = Produit.objects.filter(stockRestant__gt=0)
        #context['glaces'] = Produit.objects.filter(statut='A')
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
            uneCat = Produit.objects.filter(categorie=pk).filter(stockRestant__gt=0)
            for u in uneCat:
                glaces.append(u)
    else:
        glaces = Produit.objects.filter(categorie=p_id).filter(stockRestant__gt=0)

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
    glace = get_object_or_404(Produit, id=idGlace)
    compte = get_object_or_404(Compte, user=idClient)
    solde = compte.solde
    bacs = Bac.objects.all()

    #[0] cela retourne uniquement le premier enregistrement qu'il trouve
    mvt = Mouvement.objects.filter(produit=idGlace)[0]
    idbac = mvt.bac
    bac = get_object_or_404(Bac, libelle=idbac)
    mvt.qte = mvt.qte-1
    mvt.save()
    if mvt.qte<1:
        mvt.delete()
        """autresMouvement = Mouvement.objects.filter(produit=idGlace)
        if autresMouvement is None :
            bac.produit.delete(glace)
            glace.bac.delete(bac)"""

    tiroir = bac.tiroir
    congo = tiroir.congelateur

    t = Transaction()
    t.type = 'Achat'
    t.date = timezone.now()
    t.client = compte
    t.total = 0
    t.save()


    ligne = LigneTransaction()
    ligne.transaction = t
    ligne.produit = glace
    ligne.prix = glace.prixVente
    t.total = t.total + ligne.prix
    glace.stockRestant = glace.stockRestant - 1


    compte.solde = solde - t.total


    compte.save()
    glace.save()
    ligne.save()
    t.save()

    return render(request, 'congelateur/RecapAchat.html', {'bac': bac, 'tiroir':tiroir, 'congo':congo, 'solde':compte.solde})


def traiterDemander(request, idDemande):
    demande = get_object_or_404(Demande, id = idDemande)
    soldeSiAcceptation = demande.clientReceveur.solde - demande.montant
    return render(request, 'congelateur/traiterDemande.html',{'demande':demande, 'solde':soldeSiAcceptation})


def reponseDemande(request, demandeID):
    demande = get_object_or_404(Demande, id=demandeID)
    reponse = request.POST['reponse']
    commentaire = request.POST['commentaire']
    clientDemandeur = demande.clientDemandeur
    clientReceveur = demande.clientReceveur

    demande.commentaire = commentaire
    demande.dateReponse = datetime.datetime.now()

    if reponse =='oui':
        demande.etat = 'Acceptée'
        clientDemandeur.solde = clientDemandeur.solde + demande.montant
        clientReceveur.solde = clientReceveur.solde - demande.montant
        messages.info(request, 'Demande acceptée !')
    else:
        demande.etat = 'Refusée'
        messages.info(request, 'Demande refusée !')

    demande.save()
    clientDemandeur.save()
    clientReceveur.save()

    return dashboard(request)


def reap(request):
    listeProduits = Produit.objects.all()

    return render (request, 'congelateur/reapprovisionnement.html', {'prod':listeProduits})

def retourBac():
    bacs = Bac.objects.all()


#Méthode de réapprovisionnement
def creerReap(request):
    bacs = Bac.objects.all()
    produit = get_object_or_404(Produit, libelle=request.POST['produits'])
    qteString = request.POST['qte']
    qte = Decimal(qteString)
    prixString = request.POST['montant']
    prix = Decimal(prixString)
    userConnected = request.user
    compte = get_object_or_404(Compte, user=userConnected)

    for b in bacs:
        if qte <= (b.capaciteMax - b.nbProduit):
            produit.bac.add(b)
            b.nbProduit = b.nbProduit + qte
            break


    compte.solde = compte.solde + prix

    m = Mouvement()
    m.bac = b
    m.produit = produit
    m.qte = qte
    m.save()
    t = Transaction()
    t.type = 'Réapprovisionnement'
    t.date = timezone.now()
    t.client = compte
    t.total = 0
    t.save()

    prixParProduit = prix/qte
    i = 0
    while i < qte:
        ligne = LigneTransaction()
        ligne.transaction = t
        ligne.produit = produit
        ligne.quantite = 1
        ligne.prix = prixParProduit
        t.total = t.total + ligne.prix


        ligne.save()
        t.save()
        i = i +1

    produit.stockRestant = produit.stockRestant + qte

    produit.save()
    b.save()
    compte.save()

    return render(request, 'congelateur/confirmationEntree.html', {'bac':b, 'solde':compte.solde})


def remplissageAdmin(request):
    bacs = Bac.objects.all()
    produits = Produit.objects.all()
    return render(request, 'congelateur/RemplissageAdmin.html', {'bacs':bacs, 'produits':produits})


def EnregistrementAdmin(request):
    produit = request.POST['produits']
    p = get_object_or_404(Produit, libelle=produit)
    compte = get_object_or_404(Compte, mnemo='ADMIN')
    bac = request.POST['bacs']
    prixString = request.POST['montant']
    prix = Decimal(prixString)
    b = get_object_or_404(Bac, libelle=bac)

    qte = Decimal(request.POST['qte'])

    p.bac.add(b)
    b.nbProduit = b.nbProduit + qte


    m = Mouvement()
    m.bac = b
    m.produit = p
    m.qte = qte
    m.save()
    t = Transaction()
    t.type = 'Admin'
    t.date = timezone.now()
    t.client = compte
    t.total=0
    t.save()

    prixParProduit = prix/qte
    i = 0
    while i < qte:
        ligne = LigneTransaction()
        ligne.transaction = t
        ligne.produit = p
        ligne.quantite = 1
        ligne.prix = prixParProduit
        t.total = t.total + ligne.prix


        ligne.save()
        t.save()
        i = i +1

    p.stockRestant = p.stockRestant + qte

    p.save()
    b.save()

    return render(request, 'congelateur/accueil.html')








