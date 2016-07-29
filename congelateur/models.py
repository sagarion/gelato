from django.db import models

class Congelateur(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")
    emplacement = models.CharField(max_length=50, verbose_name="Emplacement du congélateur")


    def __str__(self):
        return self.code


class Tiroir (models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15, unique=True, verbose_name="Code")
    congelateur = models.ForeignKey(Congelateur, on_delete = models.CASCADE, related_name="tiroirs" , verbose_name="Congélateur")

    def liste(self):
        return Tiroir.objects.all()


    def __str__(self):
        return self.code

class Bac (models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")
    capaciteMax = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, verbose_name="Capacité maximum")
    nbProduit = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, verbose_name="Nombre de produits actuel")
    tiroir = models.ForeignKey(Tiroir, on_delete=models.CASCADE, verbose_name="Tiroir")

    def __str__(self):
        return self.libelle


class Produit(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=150, verbose_name="Libellé de la glace")
    image = models.ImageField(upload_to='products', verbose_name="Image", blank=True, null=True)
    categorie = models.ForeignKey('Categorie', related_name="produits", verbose_name="Catégorie de la glace")
    prixVente = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Prix de vente")
    calories = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Callories") #Maximum 5 chiffres comptant deux décimales
    ADMIN = 'AD'
    listeFourni = (
        (ADMIN, 'Admin'),
    )
    fournisseur = models.CharField(max_length=50, choices=listeFourni, default=ADMIN, verbose_name="Fournisseur")
    stockRestant = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Stock')
    bac = models.ManyToManyField(Bac, related_name="produits", blank=True, null=True)

    def __str__(self):
        return self.libelle



"""class Glace (models.Model):
        id = models.AutoField(primary_key=True)
        libelle = models.ForeignKey(LibelleGlace, on_delete=None, verbose_name="Libellé")
        datePeremption = models.DateField(auto_now=True, verbose_name="Date de péremption")
        image = models.ImageField(upload_to='products', verbose_name="Image", blank=True, null=True)
        calories = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Callories") #Maximum 5 chiffres comptant deux décimales
        prixVente = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Prix de vente")
        ADMIN = 'AD'
        listeFournisseurs = (
            (ADMIN, 'Admin'),
        )
        fournisseur = models.CharField(max_length=50, choices=listeFournisseurs, default=ADMIN, verbose_name="Fournisseur")
        bac = models.ForeignKey(Bac, verbose_name="Bac ou trouver la glace")
        cat = models.ForeignKey('Categorie', related_name="glaces", verbose_name="Catégorie de la glace")
        Avendre = 'A'
        Vendu = 'V'
        STATUT = (
            (Avendre, 'A vendre'),
            (Vendu, 'Vendue'),
        )
        statut = models.CharField(max_length=2, choices=STATUT)

"""


class Categorie (models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")
    image = models.ImageField(upload_to="categories", verbose_name="Image", blank=True, null=True)
    sousCategorie = models.ForeignKey('self', blank=True, null=True, related_name="categories", on_delete=models.CASCADE, verbose_name="Catégorie")

    def __str__(self):
        return self.libelle


class Mouvement(models.Model):
    qte = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Quantité du mouvement")
    bac = models.ForeignKey(Bac, related_name="Bac")
    produit = models.ForeignKey(Produit, related_name="Produit")

    def __str__(self):
        return str(self.qte)



