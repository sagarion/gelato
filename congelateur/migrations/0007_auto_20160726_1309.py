# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congelateur', '0006_produit_bac'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='bac',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bacs', to='congelateur.Bac', verbose_name='bac du produit'),
        ),
    ]
