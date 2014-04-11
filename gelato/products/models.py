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

# Core Django imports
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Sum

# Third-party app imports

# Gelato imports
#from transactions.models import ProductTransaction


class ProductCategory(models.Model):
    """
    A category of products that is used to group the products in order to reduce the amount of products to display at the same time.
    """
    name = models.CharField(verbose_name=_("name"), max_length=20, help_text=_("Name of the category"))
    description = models.TextField(verbose_name=_("description"), help_text=_("Description of the category"))
    picture = models.ImageField(verbose_name=_("picture"), upload_to="categories", help_text=_("Picture of the category"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the category in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the category in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('categories'), help_text=_("Last editor of the category in the database"))

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Product(models.Model):
    """
    A product (an ice cream or another product) sold through the kiosk.
    """
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("Name of the product"))
    k_name = models.CharField(verbose_name=_("kiosk name"), max_length=20, help_text=_("Product's name displayed on the kiosk client"))
    price = models.DecimalField(verbose_name=_("price"), max_digits=5, decimal_places=2, help_text=_("Sale price in CHF"))
    picture = models.ImageField(verbose_name=_("picture"), upload_to="products", help_text=_("Picture of the product"))
    k_picture = models.ImageField(verbose_name=_("kiosk picture"), upload_to="products/kiosk", help_text=_("Product's picture displayed on the kiosk client"))
    weight = models.IntegerField(verbose_name=_("weight"), max_length=4, default=0, help_text=_("Weight of the product in grams"))
    calorie = models.IntegerField(verbose_name=_("calorie"), max_length=4, default=0, help_text=_("Number of calories in a portion of the product"))
    category = models.ForeignKey('ProductCategory', verbose_name=_('category'), related_name=_('products'), help_text=_("Category the product belongs to"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the product in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the product in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('products'), help_text=_("Last editor of the product in the database"))

    def stock(self):
        # TODO: Debug stock computation
        #stock = ProductTransaction.objects.get(product=self.id).aggregate(Sum('quantity'))
        return 1 #stock

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']

    def __unicode__(self):
        return self.name