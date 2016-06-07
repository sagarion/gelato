# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 11:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('congelateur', '0020_auto_20160427_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='glace',
            name='type',
            field=models.CharField(choices=[('A', 'A vendre'), ('V', 'Vendue')], default=datetime.datetime(2016, 6, 7, 11, 54, 32, 381608, tzinfo=utc), max_length=2),
            preserve_default=False,
        ),
    ]
