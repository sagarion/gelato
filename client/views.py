from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from client.forms import ConnexionForm


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return render(request, 'congelateur/accueilConnect.html', locals())
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()


    return render(request, 'connexion.html', locals())





def deconnexion(request):
    logout(request)
    return render(request, 'congelateur/dashboard.html', locals())