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
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Third-party app imports

# Gelato imports
from products.models import Product


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
    transaction_price = models.DecimalField(verbose_name=_("total price"), max_digits=6, decimal_places=2, default=0, help_text=_("Total amount in CHF"))
    product_transaction_type = models.CharField(verbose_name=_("type of transaction"), max_length=1, choices=PRODUCT_TRANSACTION_CHOICES, default=SALE)
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(User, verbose_name=_('user'), related_name=_('product transactions'), help_text=_("User who performs the transaction"))


class FinancialTransaction(models.Model):
    """
    A debit or credit transaction made by a customer/admin
    """
    PRODUCT = 'P'
    CASH_CREDIT = 'CC'
    PAYPAL_CREDIT = 'CP'
    CASH_OUT = 'CP'
    CORRECTION = 'C'
    FINANCIAL_TRANSACTION_CHOICES = (
        (PRODUCT, _('Product transaction')),
        (CASH_CREDIT, _('Cash credit')),
        (PAYPAL_CREDIT, _('Paypal credit')),
        (CASH_OUT, _('Cash out')),
        (CORRECTION, _('Correction')),
    )

    product_transaction = models.ForeignKey('ProductTransaction', verbose_name=_('product transaction'), related_name=_('financial transaction'), blank=True, null=True, help_text=_("Product transaction"))
    amount = models.DecimalField(verbose_name=_("amount"), max_digits=6, decimal_places=2, default=0, help_text=_("Amount in CHF"))
    financial_transaction_type = models.CharField(verbose_name=_("type of transaction"), max_length=2, choices=FINANCIAL_TRANSACTION_CHOICES, default=PRODUCT)
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(User, verbose_name=_('user'), related_name=_('financial transactions'), help_text=_("User who is credited or debited"))
    banker = models.ForeignKey(User, verbose_name=_('banker'), related_name=_('banker transactions'), blank=True, null=True, help_text=_("Banker who performs the transaction"))