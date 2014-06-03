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
import random
import datetime
import pytz

# Core Django imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.db.models import Sum

# Third-party app imports
from paypal.standard.ipn.signals import payment_was_successful

# Gelato imports
from transactions.models import FinancialTransaction, ProductTransaction


logger = logging.getLogger(__name__)


class User(AbstractUser):
    card_uid = models.CharField(_("card uid"), max_length=100, null=True, blank=True)

    def balance(self):
        balance = FinancialTransaction.objects.all().filter(user=self.id).aggregate(Sum('amount'))
        return balance['amount__sum']

    def kcal(self):
        kcal = ProductTransaction.objects.all().filter(user=self.id).aggregate(Sum('kcal'))
        return kcal['kcal__sum']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class UserPin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name=_("user's pin"), help_text=_("User"))
    pin = models.IntegerField(verbose_name=_("pin code"), max_length=4, unique=True, help_text=_("One time PIN code to register user"))
    pin_creation = models.DateTimeField(verbose_name=_("created"), auto_now_add=True, help_text=_("Creation date of the PIN"))


def get_user_pin(user):
    """
    Return the pin for a given user. If the user has a pin, we return the current pin. Else, we create one unique pin
    and return it.
    :param user:
    :return pin:
    """
    # We start to check if the user already has a PIN
    try:
        pin = UserPin.objects.get(user=user).pin
        logging.debug("We already have a pin for user %s %s: %s" % (user.first_name, user.last_name, pin))
    except UserPin.DoesNotExist:
        pin = False
        logging.debug("No pin for user %s %s" % (user.first_name, user.last_name))

    # If the user has no pin, we create a new one
    if not pin:
        pin_created = False
        while not pin_created:
            try:
                pin = random.randint(1000, 9999)
                user_pin = UserPin(pin=pin, user=user)
                user_pin.save()
                pin_created = True
                pin = user_pin.pin
                logging.info("New pin created for user %s %s: %s" % (user.first_name, user.last_name, pin))
            except IntegrityError:
                pass

    return pin


def clean_user_pins():
    """
    We delete all pins that are older than 24 hours and that were not used to link an account
    :return number of pins deleted:
    """
    yesterday = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
    pins_deleted = UserPin.objects.filter(pin_creation__lt=yesterday).count()
    try:
        UserPin.objects.filter(pin_creation__lt=yesterday).delete()
    except:
        pins_deleted = 0
        logging.error("Unable to delete old user pins!")

    logging.debug("Cleaning user pins... %s pins deleted!" % pins_deleted)
    return pins_deleted


def wallet_add_money_paypal(sender, **kwargs):
    ipn_obj = sender
    logging.info('IPN request: %s' % sender)
    # You need to check 'payment_status' of the IPN

    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        user = User.objects.get(username=ipn_obj.custom)
        if user:
            transaction = FinancialTransaction()
            transaction.user = user
            transaction.amount = ipn_obj.mc_gross
            transaction.financial_transaction_type = FinancialTransaction.PAYPAL_CREDIT
            transaction.ipn_transaction = ipn_obj.txn_id
            transaction.save()
            transaction = FinancialTransaction()
            transaction.user = user
            transaction.amount = ipn_obj.mc_fee * -1
            transaction.financial_transaction_type = FinancialTransaction.PAYPAL_FEES
            transaction.ipn_transaction = ipn_obj.txn_id
            transaction.save()

payment_was_successful.connect(wallet_add_money_paypal)
