# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congelateur', '0005_delete_libelleglace'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='bac',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bacs', to='congelateur.Bac', verbose_name='bac du produit'),
            preserve_default=False,
        ),
    ]
