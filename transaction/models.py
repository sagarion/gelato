from django.contrib.auth.models import User
from django.db import models
from client.models import Compte
from congelateur.models import *
from django.db.models import Count, Min, Sum, Avg

# Create your models here.


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Date de la transaction")
    ACHAT = 'Achat'
    REAPPROVI = 'Réapprovisionnement'
    TYPE = (
        (ACHAT, 'Achat'),
        (REAPPROVI, 'Réapprovisionnement'),
    )
    type = models.CharField(max_length=30, choices=TYPE)
    image = models.ImageField(upload_to='transactions', verbose_name="Image", blank=True, null=True)
    client = models.ForeignKey(User, related_name="clients", verbose_name="Client de la transaction")
    total = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Total de transaction")


    def __str__(self):
            return str(self.date)


class LigneTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, related_name="lignes", verbose_name="Transaction")
    produit = models.ForeignKey(Produit, related_name="glace", verbose_name="Glace de la transaction")
    prix = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Montant de la ligne")
    #bac = models.ForeignKey(Bac, related_name="bacsLignes", verbose_name="bac de la ligne")


