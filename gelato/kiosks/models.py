# -*- coding: UTF-8 -*-
# models.py
#
# Copyright (C) 2014 HES-SO//HEG Arc
#
# Author(s): Cédric Gaspoz <cedric.gaspoz@he-arc.ch>
#
# This file is part of Gelato.
#
# Gelato is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gelato is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gelato. If not, see <http://www.gnu.org/licenses/>.

# Stdlib imports
import logging

# Core Django imports
from django.conf import settings
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _

# Third-party app imports

# Gelato imports
from products.models import Product


logger = logging.getLogger(__name__)


class Kiosk(models.Model):
    """
    A kiosk
    """
    name = models.CharField(verbose_name=_("name"), max_length=20, help_text=_("Name of the kiosk"))
    location = models.CharField(verbose_name=_("location"), max_length=100, help_text=_("Location of the kiosk"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_('kiosk users'), help_text=_("User account of the kiosk"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the kiosk in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the kiosk in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('kiosks'), help_text=_("Last editor of the kiosk in the database"))

    class Meta:
        verbose_name = _('kiosk')
        verbose_name_plural = _('kiosks')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class KioskStorage(models.Model):
    """
    A storage location in a kiosk
    """
    tier = models.IntegerField(verbose_name=_("tier"), max_length=1, default=0, help_text=_("Tier of a kiosk"))
    tub = models.CharField(verbose_name=_("tub"), max_length=1, blank=True, default="", help_text=_("A kiosk tub on a tier"))
    kiosk = models.ForeignKey('Kiosk', verbose_name=_('kiosk'), related_name=_('storages'), help_text=_("Kiosk the storage belongs to"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the kiosk storage in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the kiosk storage in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('kiosk storages'), help_text=_("Last editor of the kiosk storage in the database"))

    class Meta:
        verbose_name = _('kiosk storage')
        verbose_name_plural = _('kiosk storage')
        ordering = ['tier', 'tub']

    def __unicode__(self):
        return "%s%s" % (self.tier, self.tub)


def kiosk_get_available_products(kiosk):
    """
    The list of all currently available products in a given kiosk
    :param kiosk:
    :return products a queryset of products:
    """
    cursor = connection.cursor()
    SQL = """SELECT product_id FROM
    (SELECT p.product_id, SUM(p.quantity) as stock
    FROM transactions_producttransaction p
        INNER JOIN kiosks_kioskstorage s
            ON (p.storage_id = s.id)
    WHERE s.kiosk_id = %s
    GROUP BY p.product_id) AS a
    WHERE stock > 0"""
    cursor.execute(SQL, [kiosk])
    products_list = cursor.fetchall()
    products_id = []
    for id in products_list:
        products_id.append(id[0])
    products = Product.objects.filter(pk__in=products_id)
    return products


def kiosk_get_storage_location(storage):
    """
    The location of a storage in a kiosk
    :param storage:
    :return html_map:
    """
    kiosk = Kiosk.objects.get(pk=storage.kiosk.id)
    storages = KioskStorage.objects.all().filter(kiosk=kiosk.id)
    tier = None
    tubs = []
    showcase = {'tiers': [], 'max_td': 0}
    for storage in storages:
        if storage.tier != tier:
            tier = storage.tier
            showcase['tiers'].append(tier)
            showcase['max_td'] = len(tubs)
            tubs = []
            tubs.append(storage.tub)
            showcase[tier] = tubs
        else:
            tubs.append(storage.tub)
            showcase[tier] = tubs
    return showcase


def kiosk_get_product_storage(kiosk, product):
    """
    The best storage location to pick a product in a given kiosk
    :param kiosk:
    :param product:
    :return storage:
    """
    cursor = connection.cursor()
    SQL = """SELECT storage_id FROM (SELECT p.storage_id, SUM(p.quantity) as stock
    FROM transactions_producttransaction p
    INNER JOIN kiosks_kioskstorage s
    ON (p.storage_id=s.id)
    WHERE p.product_id = %s AND s.kiosk_id = %s
    GROUP BY p.product_id, p.storage_id) as A
    WHERE stock > 0
    ORDER BY stock
    """
    cursor.execute(SQL, [product.id, kiosk.id])
    storage_id = cursor.fetchone()[0]
    storage = KioskStorage.objects.get(pk=storage_id)
    return storage