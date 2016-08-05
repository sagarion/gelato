# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0013_auto_20160801_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionAnnexe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Montant')),
                ('commentaire', models.CharField(max_length=250)),
            ],
        ),
    ]
