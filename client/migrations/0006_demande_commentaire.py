# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20160725_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='commentaire',
            field=models.TextField(blank=True, null=True),
        ),
    ]