# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congelateur', '0009_produit_bac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='bac',
            field=models.ManyToManyField(related_name='produits', to='congelateur.Bac'),
        ),
    ]