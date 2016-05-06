from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    mnemo = models.CharField(max_length=15, unique=True, verbose_name="Mnemonique")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    naissance = models.DateField(verbose_name="Date de naissance")
    mail = models.EmailField(unique=True)
    solde = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Solde")
    HOMME = 'HO'
    FEMME = 'FE'
    SEXE = (
        (HOMME, 'Homme'),
        (FEMME, 'Femme'),
    )
    sexe = models.CharField(max_length=2, choices=SEXE)

    MINI = 'MINI'
    NOVICE = 'NOVICE'
    TOP = 'TOP'
    NIVEAU = (
        (MINI, 'MINI'),
        (NOVICE, 'NOVICE'),
        (TOP, 'TOP'),
    )
    niveau = models.CharField(max_length=7, choices=NIVEAU)

    ADMIN = 'AD'
    USER = 'US'
    ROLE = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )
    role = models.CharField(max_length=5,
                                      choices=ROLE)


    def __str__(self):
        return self.mnemo


class Mode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")

    def __str__(self):
        return self.libelle


class Demande(models.Model):
    id = models.AutoField(primary_key=True)
    dateDemande = models.DateField(auto_now=True, verbose_name="Date de la demande")
    montant = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Montant de la demande")
    mode = models.ForeignKey(Mode, verbose_name="Mode de paiement")
    dateReponse = models.DateField(auto_now=False, blank=True, null=True, verbose_name="Date de réponse")
    OUI = 'OUI'
    NON = 'NON'
    ON = (
        (OUI, 'Oui'),
        (NON, 'Non'),
    )
    accepte = models.CharField(max_length=2, blank=True, choices=ON)
    clientDemandeur = models.ForeignKey(Client, related_name="ClientsDemandeurs", verbose_name="Client demandeur")
    clientReceveur = models.ForeignKey(Client, related_name="ClientsReceveurs", verbose_name="Client receveur")

    def __str__(self):
        return str(self.montant)



    def VerificationDemande(self):
        if(Demande.clientReceveur.solde < Demande.montant):
            print("problème de demande")







