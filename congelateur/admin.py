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


class GlaceInline(admin.TabularInline):
    model = Glace
    fields = ('libelle', 'calories', 'prixVente')

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines = (GlaceInline,)
    list_display = ('code', 'libelle', 'sousCategorie')

class GlaceAdmin(admin.ModelAdmin):
    model = Glace
    list_display = ('libelle',)



admin.site.register(Congelateur, CongelateurAdmin)
admin.site.register(Tiroir, TiroirAdmin)
admin.site.register(Bac)
admin.site.register(Glace, GlaceAdmin)
admin.site.register(Categorie, CategorieAdmin)