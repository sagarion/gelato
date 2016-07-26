from dal import autocomplete
from django import forms
from client.models import *

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ("clientReceveur", 'montant', 'mode')
        labels = {
            'clientReceveur':('Demander la somme à'),
            'montant':('Montant souhaité'),
            'mode':('Je rembourse à l\'aide de')
        }



        """widgets = {
            "clientReceveur":autocomplete.ModelSelect2(url='client-autocomplete')
        }"""


class TraiterDemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ('montant','etat', 'commentaire')
        labels = {
            'montant':('Montant envoyé'),
            'etat':('Accepter la demande ?'),
            'commentaire':('Ajouter un commentaire')
        }