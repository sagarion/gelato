from dal import autocomplete
from django import forms
from client.models import *

class DemandeForm(forms.ModelForm):

    Compte.clientReceveur = forms.ModelChoiceField(
        queryset=Compte.objects.all(),
        widget=autocomplete.ModelSelect2(url='client-autocomplete'))

    class Meta:
        model = Demande
        fields = ("clientReceveur", 'montant', 'mode')
        labels = {
            'clientReceveur':('Demander la somme à'),
            'montant':('Montant souhaité'),
            'mode':('Je rembourse à l\'aide de')
        }

"""
        help_texts = {
            'mode': ('Méthode que vous utiliserez pour rembourser votre partenaire'),
        }
"""
