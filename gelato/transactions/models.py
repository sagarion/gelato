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


# Third-party app imports

# Gelato imports
from products.models import Product
from kiosks.models import KioskStorage


class ProductTransaction(models.Model):
    """
    A sale or replenishment transaction made by a customer/admin of the kiosk
    """
    SALE = 'S'
    REPLENISH = 'R'
    INVENTORY = 'I'
    PRODUCT_TRANSACTION_CHOICES = (
        (SALE, _('Sale')),
        (REPLENISH, _('Replenish')),
        (INVENTORY, _('Inventory')),
    )

    product = models.ForeignKey(Product, verbose_name=_("product"), related_name=_("transactions"), help_text=_("Product sold or replenished"))
    quantity = models.IntegerField(verbose_name=_("quantity"), max_length=4, default=0, help_text=_("Quantity sold or replenished"))
    storage = models.ForeignKey(KioskStorage, verbose_name=_('kiosk storage'), related_name=_('products'), help_text=_("Storage location of a product in a kiosk"))
    transaction_price = models.DecimalField(verbose_name=_("total price"), max_digits=6, decimal_places=2, default=0, help_text=_("Total amount in CHF"))
    product_transaction_type = models.CharField(verbose_name=_("type of transaction"), max_length=1, choices=PRODUCT_TRANSACTION_CHOICES, default=SALE)
    kcal = models.IntegerField(verbose_name=_("kcal"), max_length=8, default=0, help_text=_("Automatically updated when the transaction is saved"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_('product transactions'), help_text=_("User who performs the transaction"))

    def abs_quantity(self):
        return abs(self.quantity)

    class Meta:
        verbose_name = _('product transaction')
        verbose_name_plural = _('product transactions')
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.kcal = self.product.calorie * self.quantity
        super(ProductTransaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s (%sx)" % (self.product, abs(self.quantity))


class FinancialTransaction(models.Model):
    """
    A debit or credit transaction made by a customer/admin
    """
    PRODUCT = 'P'
    CASH_CREDIT = 'CC'
    PAYPAL_CREDIT = 'CP'
    PAYPAL_FEES = 'CF'
    CASH_OUT = 'CO'
    CORRECTION = 'C'
    FINANCIAL_TRANSACTION_CHOICES = (
        (PRODUCT, _('Product transaction')),
        (CASH_CREDIT, _('Cash credit')),
        (PAYPAL_CREDIT, _('PayPal credit')),
        (PAYPAL_FEES, _('PayPal fees')),
        (CASH_OUT, _('Cash out')),
        (CORRECTION, _('Correction')),
    )

    product_transaction = models.ForeignKey('ProductTransaction', verbose_name=_('product transaction'), related_name=_('financial transaction'), blank=True, null=True, help_text=_("Product transaction"))
    amount = models.DecimalField(verbose_name=_("amount"), max_digits=6, decimal_places=2, default=0, help_text=_("Amount in CHF"))
    financial_transaction_type = models.CharField(verbose_name=_("type of transaction"), max_length=2, choices=FINANCIAL_TRANSACTION_CHOICES, default=PRODUCT)
    ipn_transaction = models.CharField(verbose_name=_("IPN transaction ID"), max_length=20, default="", help_text=_("PayPal's IPN transaction ID"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_('financial transactions'), help_text=_("User who is credited or debited"))
    banker = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('banker'), related_name=_('banker transactions'), blank=True, null=True, help_text=_("Banker who performs the transaction"))

    class Meta:
        verbose_name = _('financial transaction')
        verbose_name_plural = _('financial transactions')
        ordering = ['-created']

    def __unicode__(self):
        return "%s [%s] %s (%s)" % (self.created.strftime("%Y-%m-%d %H:%M:%S"), self.financial_transaction_type, self.user, self.amount)