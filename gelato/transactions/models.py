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
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Third-party app imports

# Gelato imports
from products.models import Product
from kiosks.models import KioskStorage, kiosk_get_product_storage


logger = logging.getLogger(__name__)


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
    lock_open = models.BooleanField(verbose_name=_("lock opened"), default=False, help_text=_("Lock was opened"))
    door_open = models.BooleanField(verbose_name=_("door opened"), default=False, help_text=_("Door was opened"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_('product_transactions'), help_text=_("User who performs the transaction"))

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

    product_transaction = models.ForeignKey('ProductTransaction', verbose_name=_('product transaction'), related_name=_('financial_transaction'), blank=True, null=True, help_text=_("Product transaction"))
    amount = models.DecimalField(verbose_name=_("amount"), max_digits=6, decimal_places=2, default=0, help_text=_("Amount in CHF"))
    financial_transaction_type = models.CharField(verbose_name=_("type of transaction"), max_length=2, choices=FINANCIAL_TRANSACTION_CHOICES, default=PRODUCT)
    ipn_transaction = models.CharField(verbose_name=_("IPN transaction ID"), max_length=20, default="", help_text=_("PayPal's IPN transaction ID"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now=True, help_text=_("Date of the transaction"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_('financial_transactions'), help_text=_("User who is credited or debited"))
    banker = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('banker'), related_name=_('banker_transactions'), blank=True, null=True, help_text=_("Banker who performs the transaction"))

    class Meta:
        verbose_name = _('financial transaction')
        verbose_name_plural = _('financial transactions')
        ordering = ['-created']

    def __unicode__(self):
        return "%s [%s] %s (%s)" % (self.created.strftime("%Y-%m-%d %H:%M:%S"), self.financial_transaction_type, self.user, self.amount)


def product_sale_transaction(kiosk, product, user):
    if user.balance() >= product.price:
        try:
            storage = kiosk_get_product_storage(kiosk, product)

            product_transaction = ProductTransaction()
            product_transaction.product = product
            product_transaction.quantity = -1
            product_transaction.transaction_price = product.price*-1
            product_transaction.product_transaction_type = ProductTransaction.SALE
            product_transaction.user = user
            product_transaction.storage = storage
            product_transaction.save()

            financial_transaction = FinancialTransaction()
            financial_transaction.product_transaction = product_transaction
            financial_transaction.amount = product_transaction.transaction_price
            financial_transaction.ipn_transaction = "None"
            financial_transaction.user = user
            financial_transaction.banker = kiosk.user
            financial_transaction.save()
            return product_transaction
        except:
            return False
    return False


def check_transaction(transaction_id, user):
    success = False

    try:
        transaction = ProductTransaction.objects.get(pk=transaction_id)
        if transaction.storage.kiosk.user != user:
            message = 'Check transaction %s: INVALID USER' % transaction_id
            success = False
            logging.info(message)
        if not transaction.lock_open:
            transaction.lock_open = True
            transaction.save()
            message = 'Check transaction %s: VALID' % transaction_id
            success = True
            logging.info(message)
        else:
            message = 'Check transaction %s: ALREADY OPEN' % transaction_id
            success = False
            logging.warning(message)
    except ProductTransaction.DoesNotExist:
        message = 'Check transaction %s: NOT EXIST' % transaction_id
        success = False
        logging.error(message)

    return success, message