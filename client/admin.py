from django.contrib import admin
from client.models import *
from congelateur.forms import DemandeForm

class ClientAdmin(admin.ModelAdmin):
    list_display = ('mnemo', 'prenom', 'nom', 'solde')

"""class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'clientDemandeur', 'clientReceveur', 'montant', 'mode', 'accepte', 'dateDemande')
  """
class DemandeAdmin(admin.ModelAdmin):
    form = DemandeForm

admin.site.register(Client, ClientAdmin)
admin.site.register(Demande, DemandeAdmin)
admin.site.register(Mode)
admin.site.register(Compte)