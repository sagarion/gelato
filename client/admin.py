from django.contrib import admin
from client.models import *

class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'clientDemandeur', 'clientReceveur', 'montant', 'mode', 'etat', 'dateDemande')

class CompteAdmin(admin.ModelAdmin):
    list_display = ('prenom','nom','solde', 'niveau')
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('libelle','nbTransactionMinimum')

admin.site.register(Demande, DemandeAdmin)
admin.site.register(Mode)
admin.site.register(Compte, CompteAdmin)
admin.site.register(Niveau, NiveauAdmin)