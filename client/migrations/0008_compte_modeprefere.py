# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-15 11:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_compte'),
    ]

    operations = [
        migrations.AddField(
            model_name='compte',
            name='modePrefere',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='modePrefere', to='client.Mode', verbose_name='Mode de remboursement préféré'),
            preserve_default=False,
        ),
    ]
