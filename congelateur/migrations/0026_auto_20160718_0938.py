# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-18 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congelateur', '0025_auto_20160622_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glacee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calories', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Callories')),
                ('datePeremption', models.DateField(auto_now=True, verbose_name='Date de péremption')),
                ('fournisseur', models.CharField(choices=[('AD', 'Admin')], default='AD', max_length=50, verbose_name='Fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Image')),
                ('prixVenteConseille', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Prix de vente')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='congelateur.Categorie', verbose_name='Catégorie de la glace')),
                ('libelle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='congelateur.LibelleGlace', verbose_name='Libellé')),
            ],
        ),
        migrations.AddField(
            model_name='glacee',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glaces', to='congelateur.Produit', verbose_name='Produit'),
        ),
    ]
