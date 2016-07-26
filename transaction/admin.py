from django.contrib import admin
from transaction.models import *

# Register your models here.



class LigneInline(admin.TabularInline):
    model = LigneTransaction
    fields = ('produit', 'prix', 'bac')



class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('date', 'type','client','total')
    inlines = (LigneInline,)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LigneTransaction)