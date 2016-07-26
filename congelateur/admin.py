from django.contrib import admin

from congelateur.forms import BacForm
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

class ProduitAdmin(admin.ModelAdmin):
     model= Produit
     filter_horizontal = ('bac',)


class BacAdmin(admin.ModelAdmin):

  form = BacForm
  list_display = ('libelle', 'nbProduit', 'capaciteMax', 'tiroir')

  fieldsets = (
    (None, {'fields': ('libelle','nbProduit', 'capaciteMax', 'tiroir', 'produits')}),
  )

class MouvementAdmin(admin.ModelAdmin):
    model = Mouvement
    list_display = ('qte','bac', 'produit')
    fieldsets = (
    (None, {'fields': ('qte','bac', 'produit')}),
    )

admin.site.register(Congelateur, CongelateurAdmin)
admin.site.register(Tiroir, TiroirAdmin)
admin.site.register(Bac, BacAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Mouvement, MouvementAdmin)