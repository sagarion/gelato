from dal import autocomplete
from django import forms
from client.models import *
from congelateur.models import Produit


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





class BacForm(forms.ModelForm):

  produits = forms.ModelMultipleChoiceField(
    Produit.objects.all(),
# Add this line to use the double list widget
#    widget=admin.widgets.FilteredSelectMultiple('Produits', False),
    required=False,
  )

  def __init__(self, *args, **kwargs):
    super(BacForm, self).__init__(*args, **kwargs)
    if self.instance.pk:
      #if this is not a new object, we load related produits
      self.initial['produits'] = self.instance.produits.values_list('pk', flat=True)

  def save(self, *args, **kwargs):
    instance = super(BacForm, self).save(*args, **kwargs)
    if instance.pk:
      for prod in instance.produits.all():
        if prod not in self.cleaned_data['produits']:
          # we remove produits which have been unselected
          instance.produits.remove(prod)
      for prod in self.cleaned_data['produits']:
        if prod not in instance.produits.all():
          # we add newly selected produits
          instance.produits.add(prod)
    return instance