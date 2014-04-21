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
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

# Third-party app imports
from paypal.standard.ipn.signals import payment_was_successful

# Gelato imports
from transactions.models import FinancialTransaction


class User(AbstractUser):
    card_uid = models.CharField(_("card uid"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


def wallet_add_money_paypal(sender, **kwargs):
    ipn_obj = sender
    # You need to check 'payment_status' of the IPN

    if ipn_obj.payment_status == "Completed":
        # Undertake some action depending upon `ipn_obj`.
        user = User.objects.get(username=ipn_obj.custom)
        if user:
            transaction = FinancialTransaction()
            transaction.user = user
            transaction.amount = ipn_obj.auth_amount
            transaction.financial_transaction_type = FinancialTransaction.PAYPAL_CREDIT
            transaction.save()

payment_was_successful.connect(wallet_add_money_paypal)
