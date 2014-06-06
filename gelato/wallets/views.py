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
import json
import logging

# Core Django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Sum
#from django.contrib.auth.models import User
from django.conf import settings
from django.db import DataError


# Third-party app imports
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
#from reportlab.graphics.barcode import code39
from paypal.standard.forms import PayPalPaymentsForm

# Gelato imports
from transactions.models import ProductTransaction, FinancialTransaction
from .models import User, UserPin, clean_user_pins, get_user_pin, activate_account_rfid


logger = logging.getLogger(__name__)


class UserListView(ListView):
    model = User
    # TODO: Request admin login


class UserDetail(DetailView):
    model = User
    # TODO: Request admin login

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['product_transaction_list'] = ProductTransaction.objects.all().filter(user=self.object)
        context['financial_transaction_list'] = FinancialTransaction.objects.all().filter(user=self.object)
        return context


@login_required()
def dashboard(request):
    user = request.user
    if not user.is_active:
        return HttpResponseRedirect(reverse('create_account'))

    financial_transactions = FinancialTransaction.objects.all().filter(user=user).select_related('product')
    product_transactions = ProductTransaction.objects.all().filter(user=user).select_related('product')
    return render_to_response('wallets/dashboard.html', {"financial_transactions": financial_transactions,
                                                         "product_transactions": product_transactions,
                                                         "user": user, }, context_instance=RequestContext(request))


@login_required()
def create_account(request):
    user = request.user
    #if user.is_active:
    #    return HttpResponseRedirect(reverse('dashboard'))

    pin = get_user_pin(user)

    return render_to_response('wallets/create_account.html', {"user": user, "pin": pin}, context_instance=RequestContext(request))


@login_required()
def activation_form(request):
    user = request.user
    if user.is_active:
        return HttpResponseRedirect(reverse('dashboard'))

    pin = get_user_pin(user)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="gelato-activation-form.pdf"; size=A4'

    p = canvas.Canvas(response)

    p.drawImage('%s/img/wallets/activation-form.jpg' % settings.STATIC_ROOT, 0, 0, width=210*mm, height=297*mm)

    # TODO: Center barcode
    p.setFont('Helvetica', 48)
    p.drawString(90*mm, 80*mm, "%s" % pin)
    #barcode = code39.Extended39('%s' % user.username.split('@')[0], barWidth=0.5*mm, barHeight=20*mm)
    #barcode.drawOn(p, 60*mm, 80*mm)

    p.setFont('Helvetica', 12)
    p.drawString(12.6*mm, 244*mm, "Bienvenue %s %s!" % (user.first_name, user.last_name))

    p.setFont('Helvetica', 9)
    p.drawString(152*mm, 111*mm, "%s %s" % (user.first_name, user.last_name))
    p.drawString(152*mm, 108*mm, "UID: %s" % user.username.split('@')[0])

    p.showPage()
    p.save()

    return response


@require_GET
def rfid_scan(request, kiosk_id, rfid):
    request.session['rfid'] = rfid
    request.session['kiosk_id'] = int(kiosk_id)
    if rfid == 'ESC':
        # The card is gone, we need to log-out
        try:
            del request.session['kiosk_user']
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('kiosk_home'))
    try:
        user = User.objects.get(card_uid=rfid)
        request.session['kiosk_user'] = user.id
        return HttpResponseRedirect(reverse('kiosk_showcase'))
    except User.DoesNotExist:
        #We need to link the account
        logging.info("The card %s is not known." % rfid)
        return HttpResponseRedirect(reverse('kiosk_unknown_rfid'))


@csrf_exempt
@require_POST
def activate_account(request):
    # TODO: Force login from Kiosk
    user = None
    pin = request.POST.get("pin", "")
    card_uid = request.POST.get("card_uid", "")
    if pin and card_uid:
        user = activate_account_rfid(card_uid, pin)
        try:
            user_pin = UserPin.objects.get(pin=pin)
            user = user_pin.user
        except UserPin.DoesNotExist:
            logger.error("UserPin does not exist! Invalid PIN: %s." % pin)

    result = {}
    if user:
        try:
            user.card_uid = card_uid
            user.is_active = 1
            user.save()
            user_pin.delete()
            account = {}
            account['username'] = user.username
            account['first_name'] = user.first_name
            account['last_name'] = user.last_name
            account['card_uid'] = user.card_uid
            result['account'] = account
            result['message'] = "Votre carte a été activée. Vous pouvez utiliser gelato dès à présent!"
            result['success'] = True
            logger.info("Card UID [%s] activated for user [%s]" % (user.card_uid, user.username))
        except DataError:
            result['message'] = "Nous n'avons pas pu enregistrer votre carte. Veuillez vous adresser au bureau 150."
            result['success'] = False
            logger.error("DataError {'pin': %s, 'card_uid': %s}" % (pin, card_uid))
    else:
        result['message'] = "Nous n'avons pas pu enregistrer votre carte. Veuillez vous adresser au bureau 150."
        result['success'] = False
        logger.error("Invalid data received {'pin': %s, 'card_uid': %s}" % (pin, card_uid))
    return HttpResponse(json.dumps(result),  content_type="application/json")


@login_required()
def wallet_add_money_paypal(request):
    user = request.user
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "20.00",
        "item_name": "Gelato Kiosk",
        "currency_code": "CHF",
        "lc": "CH",
        "no_shipping": "1",
        "custom": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        #"invoice": "unique-invoice-id",
        "notify_url": "https://marmix.ig.he-arc.ch" + reverse('paypal-ipn'),
        "return_url": "https://marmix.ig.he-arc.ch" + reverse('paypal-return'),
        "cancel_return": "https://marmix.ig.he-arc.ch" + reverse('paypal-cancel'),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "user": user}
    return render_to_response("wallets/paypal_submit.html", context)


@login_required()
# TODO: Require admin
def wallet_add_money_cash(request):
    pass


def cron_clean_user_pins(request):
    cleaned_pins = clean_user_pins()
    response = HttpResponse("%s PINS were successfully deleted!" % cleaned_pins, content_type="text/plain")
    return response


class UserHomeDetail(TemplateView):
    template_name = "wallets/home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserHomeDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserHomeDetail, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context