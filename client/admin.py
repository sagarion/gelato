from django.contrib import admin
from client.models import *

class ClientAdmin(admin.ModelAdmin):
    list_display = ('mnemo', 'prenom', 'nom', 'solde')

class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'clientDemandeur', 'clientReceveur', 'montant', 'mode', 'accepte', 'dateDemande')


admin.site.register(Client, ClientAdmin)
admin.site.register(Demande, DemandeAdmin)
admin.site.register(Mode)