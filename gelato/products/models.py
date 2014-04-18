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


class ProductSupplier(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, help_text=_("Name of the supplier"))
    contact = models.CharField(verbose_name=_("contact"), max_length=50, blank=True, default="", help_text=_("Supplier's contact person"))
    address_street = models.CharField(verbose_name=_("street address"), max_length=50, blank=True, default="", help_text=_("Supplier's street address"))
    address_zip = models.CharField(verbose_name=_("zip"), max_length=4, blank=True, default="", help_text=_("Supplier's zip"))
    address_city = models.CharField(verbose_name=_("city"), max_length=50, blank=True, default="", help_text=_("Supplier's city"))
    contact_phone = models.CharField(verbose_name=_("contact phone"), max_length=10, blank=True, default="", help_text=_("Phone number of the contact"))
    contact_email = models.EmailField(verbose_name=_("contact email"), max_length=80, blank=True, default="", help_text=_("Email address of the contact"))
    order_email = models.EmailField(verbose_name=_("order email"), max_length=80, blank=True, default="", help_text=_("Email address used to send orders (can be the same as contact email)"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the category in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the category in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('suppliers'), help_text=_("Last editor of the category in the database"))

    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ['name']

    def __unicode__(self):
        if self.contact != "":
            return "%s (%s)" % (self.name, self.contact)
        else:
            return self.name


class ProductBrand(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=20, help_text=_("Name of the brand"))
    logo = models.ImageField(verbose_name=_("logo"), upload_to="brands", help_text=_("Logo of the brand"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the category in the database"))
    edited = models.DateTimeField(verbose_name=_("edited"), auto_now=True, help_text=_("Last edition of the category in the database"))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('editor'), related_name=_('brands'), help_text=_("Last editor of the category in the database"))

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')
        ordering = ['name']

    def __unicode__(self):
        return self.name


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
    # TODO: Add product position in the freezer
    product_code = models.CharField(verbose_name=_("product code"), max_length=30, blank=True, default="", help_text=_("Code used to order this product from it's supplier"))
    ean = models.CharField(verbose_name=_("EAN"), max_length=18, blank=True, default="", help_text=_("EAN code (barcode) of the product"))
    tu = models.IntegerField(verbose_name=_("trade units"), max_length=3, default=1, help_text=_("Quantity of units per trade unit"))
    name = models.CharField(verbose_name=_("name"), max_length=100, help_text=_("Name of the product"))
    k_name = models.CharField(verbose_name=_("kiosk name"), max_length=20, help_text=_("Product's name displayed on the kiosk client"))
    price = models.DecimalField(verbose_name=_("price"), max_digits=5, decimal_places=2, help_text=_("Sale price in CHF"))
    picture = models.ImageField(verbose_name=_("picture"), upload_to="products", help_text=_("Picture of the product"))
    k_picture = models.ImageField(verbose_name=_("kiosk picture"), upload_to="products/kiosk", help_text=_("Product's picture displayed on the kiosk client"))
    weight = models.IntegerField(verbose_name=_("weight"), max_length=4, default=0, help_text=_("Weight of the product in grams"))
    calorie = models.IntegerField(verbose_name=_("calorie"), max_length=4, default=0, help_text=_("Number of calories in a portion of the product"))
    category = models.ForeignKey('ProductCategory', verbose_name=_('category'), related_name=_('products'), help_text=_("Category the product belongs to"))
    brand = models.ForeignKey('ProductBrand', verbose_name=_('brand'), related_name=_('products'), help_text=_("Brand of the product"))
    supplier = models.ForeignKey('ProductSupplier', verbose_name=_('supplier'), related_name=_('products'), help_text=_("Supplier of the product"))
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