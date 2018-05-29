# -*- coding: UTF-8 -*-
# views.py
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
import json

# Core Django imports
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

# Third-party app imports

# Gelato imports
from wallets.models import activate_account_rfid, User
from transactions.models import ProductTransaction, product_sale_transaction, check_transaction
from kiosks.models import Kiosk, kiosk_get_available_products, kiosk_get_storage_location
from products.models import Product

logger = logging.getLogger(__name__)


def kiosk_home(request):
    return render(request,'kiosk/home.html', {})


def kiosk_unknown_rfid(request):
    return render(request,'kiosk/unknown.html', {})


def kiosk_associate_rfid(request):
    rfid = request.session.get('rfid', False)
    if request.method == 'POST':
        pin = request.POST.get("pin", "")
        user = activate_account_rfid(rfid, pin)
        if user:
            if user.card_uid:
                request.session['kiosk_user'] = user.id
                return HttpResponseRedirect(reverse('kiosk_showcase'))
        else:
            message = """Le PIN que vous avez entré n'est pas ou n'est plus valide. Nous vous invitons à imprimer un
                      nouveau formulaire d'activation depuis le site Gelato et de recommencer la procédure. En cas
                      d'erreur répétée, veuillez vous adresser au bureau 150."""
            error = {'title': "PIN non valide", 'message': message}
            return render(request,'kiosk/error.html', {'error': error, })
    else:
        return render(request,'kiosk/associate_rfid.html', {'rfid': rfid, })


def kiosk_showcase(request):
    user_id = request.session.get('kiosk_user', False)
    if not user_id:
        message = """L'authentification au moyen de votre badge a échoué ou a été révoquée. Veuillez retirer et replacer
                     votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Authentification révoquée", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    user = User.objects.get(pk=user_id)
    product_transactions = ProductTransaction.objects.all().filter(user=user).select_related('product')
    products = kiosk_get_available_products(1)
    return render(request, 'kiosk/showcase.html', {'user': user, 'product_transactions': product_transactions,
                                                      'products': products})


def kiosk_select(request, product_id):
    user_id = request.session.get('kiosk_user', False)
    if not user_id:
        message = """L'authentification au moyen de votre badge a échoué ou a été révoquée. Veuillez retirer et replacer
                     votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Authentification révoquée", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    user = User.objects.get(pk=user_id)
    product = Product.objects.select_related().get(pk=product_id)
    product_transactions = ProductTransaction.objects.all().filter(user=user).select_related('product')
    if user.balance() > product.price:
        sell = True
    else:
        sell = False
    return render('kiosk/select.html', {'user': user, 'product': product, 'sell': sell,
                                                    'product_transactions': product_transactions})


def kiosk_sell(request, product_id):
    user_id = request.session.get('kiosk_user', False)
    kiosk_id = request.session.get('kiosk_id', False)
    logging.debug("Kiosk Sell > USER: %s | KIOSK: %s" % (user_id, kiosk_id))
    if not user_id or not kiosk_id:
        message = """L'authentification au moyen de votre badge a échoué ou a été révoquée. Veuillez retirer et replacer
                     votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Authentification révoquée", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    user = User.objects.get(pk=user_id)
    kiosk = Kiosk.objects.get(pk=kiosk_id)
    product = Product.objects.select_related().get(pk=product_id)
    transaction = product_sale_transaction(kiosk, product, user)
    if not transaction:
        message = """La transaction a échoué! Veuillez retirer et replacer votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Transaction annulée", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    product_transactions = ProductTransaction.objects.all().filter(user=user).select_related('product') # TODO: .distinct('product')
    showcase = kiosk_html_showcase(transaction.storage)
    return render(request, 'kiosk/sell.html', {'user': user, 'product': product, 'transaction': transaction,
                                                    'showcase': showcase, 'product_transactions': product_transactions})


def kiosk_exit(request):
    try:
        del request.session['kiosk_user']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('kiosk_home'))


def kiosk_error(request):
    return render(request,'kiosk/error.html', {})


@login_required()
def kiosk_check_transaction(request, transaction_id):
    # We need the Kiosk user to check if the transaction was initiated from this user
    user = request.user
    success, message = check_transaction(transaction_id, user)
    if success:
        transaction = ProductTransaction.objects.get(pk=transaction_id)
        location = transaction.storage.tier
    else:
        location = None
    result = {'success': success, 'message': message, 'location': location}
    return HttpResponse(json.dumps(result),  content_type="application/json")


@login_required()
def kiosk_check_admin(request, user_id):
    success = False
    message = 'Unprivileged user'
    # We need the Kiosk user to check if the transaction was initiated from this user
    user = User.objects.get(pk=user_id)
    if user:
        if user.is_superuser:
            success = True
            message = "Privilege successfully checked"
    result = {'success': success, 'message': message, }
    return HttpResponse(json.dumps(result),  content_type="application/json")


def kiosk_admin(request):
    user_id = request.session.get('kiosk_user', False)
    if not user_id:
        message = """L'authentification au moyen de votre badge a échoué ou a été révoquée. Veuillez retirer et replacer
                     votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Authentification révoquée", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    user = User.objects.get(pk=user_id)
    if not user.is_superuser:
        message = """Vous n'avez pas les droits suffisants pour accéder à cette page. En cas d'erreur répétée, veuillez
        vous adresser au bureau 150."""
        error = {'title': "Privilèges insuffisants", 'message': message}
        return render(request,'kiosk/error.html', {'error': error, })
    return render(request,'kiosk/admin.html', {'user': user, })

def kiosk_html_showcase(storage):
    showcase = kiosk_get_storage_location(storage)
    html = """<div class="kiosk-table">"""
    for tier in showcase['tiers']:
        html += """<div class="kiosk-row">"""
        for tub in showcase[tier]:
            if storage.tier == tier and storage.tub == tub:
                html += """<div class="kiosk-cell kiosk-storage">%s%s</div>""" % (tier, tub)
            else:
                html += """<div class="kiosk-cell">%s%s</div>""" % (tier, tub)
        html += """</div>"""
    html += """</div>"""
    return html