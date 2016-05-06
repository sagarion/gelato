from django import forms
from django.contrib import admin

from congelateur.models import *


class CongelateurAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle', 'emplacement')


admin.site.register(Congelateur, CongelateurAdmin)
admin.site.register(Tiroir)
admin.site.register(Bac)
admin.site.register(Glace)
admin.site.register(Categorie)