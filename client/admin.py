from django.contrib import admin
from client.models import *

class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'clientDemandeur', 'clientReceveur', 'montant', 'mode', 'etat', 'dateDemande')

admin.site.register(Demande, DemandeAdmin)
admin.site.register(Mode)
admin.site.register(Compte)
admin.site.register(Niveau)