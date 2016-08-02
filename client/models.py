from django.db import models
from django.contrib.auth.models import User




class Mode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")

    def __str__(self):
        return self.libelle


class Niveau(models.Model):
    class Meta:
        verbose_name_plural = "Niveaux"
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100, verbose_name="Libellé")

    def __str__(self):
        return self.libelle


class Compte(models.Model):
    user = models.OneToOneField(User)
    mnemo = models.CharField(max_length=15, unique=True, verbose_name="Mnemonique")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    naissance = models.DateField(verbose_name="Date de naissance")
    mail = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, verbose_name="Téléphone", null=True, blank=True)
    solde = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Solde")
    HOMME = 'Homme'
    FEMME = 'Femme'
    SEXE = (
        (HOMME, 'Homme'),
        (FEMME, 'Femme'),
    )
    sexe = models.CharField(max_length=20, choices=SEXE)
    niveau = models.ForeignKey(Niveau,verbose_name="Niveau")
    modePrefere = models.ForeignKey(Mode, related_name="modePrefere", verbose_name="Mode de remboursement préféré")

    ADMIN = 'AD'
    USER = 'US'
    ROLE = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )
    role = models.CharField(max_length=5,
                                      choices=ROLE)


    def __str__(self):
        return "{0} {1}".format(self.prenom, self.nom)




class Demande(models.Model):
    id = models.AutoField(primary_key=True)
    dateDemande = models.DateField(auto_now=True, verbose_name="Date de la demande")
    montant = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Montant de la demande")
    mode = models.ForeignKey(Mode, verbose_name="Mode de paiement")
    dateReponse = models.DateField(auto_now=False, blank=True, null=True, verbose_name="Date de réponse")
    EnAttente = 'En attente'
    Acceptee = 'Acceptée'
    Refusee = 'Refusée'
    ON = (
        (EnAttente, 'En attente'),
        (Acceptee, 'Acceptée'),
        (Refusee, 'Refusée'),
    )
    etat = models.CharField(max_length=20, blank=True, choices=ON)
    clientDemandeur = models.ForeignKey(Compte, related_name="ClientsDemandeurs", verbose_name="Client demandeur")
    clientReceveur = models.ForeignKey(Compte, related_name="ClientsReceveurs", verbose_name="Client receveur")
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.montant)



    def VerificationDemande(self):
        if(Demande.clientReceveur.solde < Demande.montant):
            print("problème de demande")







