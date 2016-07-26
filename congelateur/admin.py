from django import forms
from django.contrib import admin

from congelateur.models import *


class TiroirInline(admin.TabularInline):
    model = Tiroir
    fields = ('code', )

class CongelateurAdmin(admin.ModelAdmin):
    model = Congelateur
    inlines = (TiroirInline,)
    list_display = ('code', 'libelle', 'emplacement')


class BacInline(admin.TabularInline):
    model = Bac
    fields = ('code', 'libelle' )

class TiroirAdmin(admin.ModelAdmin):
    model = Tiroir
    inlines = (BacInline,)


class ProduitInline(admin.TabularInline):
    model = Produit
    fields = ('libelle',)

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines = (ProduitInline,)
    list_display = ('code', 'libelle', 'sousCategorie')

class BacAdmin(admin.ModelAdmin):
    model = Bac
    list_display = ('libelle','tiroir','capaciteMax','nbProduit')

"""class GlaceAdmin(admin.ModelAdmin):
    model = Glace
    list_display = ('produit','datePeremption','fournisseur')


class GlaceInline(admin.TabularInline):
    model = Glace
    fields = ('datePeremption', 'fournisseur')

class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    inlines = (GlaceInline, )
    list_display = ('libelle', 'image', 'categorie', 'prixVenteConseille','calories', 'stockRestant', 'bac')
"""


admin.site.register(Congelateur, CongelateurAdmin)
admin.site.register(Tiroir, TiroirAdmin)
admin.site.register(Bac, BacAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Produit)