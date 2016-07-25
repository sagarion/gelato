# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bac',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5, unique=True, verbose_name='Code')),
                ('libelle', models.CharField(max_length=100, verbose_name='Libellé')),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=5, unique=True, verbose_name='Code')),
                ('libelle', models.CharField(max_length=100, verbose_name='Libellé')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories', verbose_name='Image')),
                ('sousCategorie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='congelateur.Categorie', verbose_name='Catégorie')),
            ],
        ),
        migrations.CreateModel(
            name='Congelateur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=15, unique=True, verbose_name='Code')),
                ('libelle', models.CharField(max_length=100, verbose_name='Libellé')),
                ('emplacement', models.CharField(max_length=50, verbose_name='Emplacement du congélateur')),
            ],
        ),
        migrations.CreateModel(
            name='Glace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datePeremption', models.DateField(verbose_name='Date de péremption')),
                ('fournisseur', models.CharField(choices=[('AD', 'Admin')], default='AD', max_length=50, verbose_name='Fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='LibelleGlace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=150, verbose_name='Libellé de la glace')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=150, verbose_name='Libellé de la glace')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Image')),
                ('prixVenteConseille', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Prix de vente')),
                ('calories', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Callories')),
                ('stockRestant', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Stock')),
                ('bac', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='congelateur.Bac', verbose_name='Bac ou trouver la glace')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='congelateur.Categorie', verbose_name='Catégorie de la glace')),
            ],
        ),
        migrations.CreateModel(
            name='Tiroir',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=15, unique=True, verbose_name='Code')),
                ('congelateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiroirs', to='congelateur.Congelateur', verbose_name='Congélateur')),
            ],
        ),
        migrations.AddField(
            model_name='glace',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glaces', to='congelateur.Produit', verbose_name='Produit'),
        ),
        migrations.AddField(
            model_name='bac',
            name='tiroir',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='congelateur.Tiroir', verbose_name='Tiroir'),
        ),
    ]
