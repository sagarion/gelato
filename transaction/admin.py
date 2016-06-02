from django.contrib import admin
from transaction.models import *

# Register your models here.



class LigneInline(admin.TabularInline):
    model = LigneTransaction
    fields = ('glace', 'prix')



class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    inlines = (LigneInline,)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LigneTransaction)