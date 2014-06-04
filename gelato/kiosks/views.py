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

# Core Django imports
from django.shortcuts import render_to_response, get_object_or_404
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
from transactions.models import ProductTransaction

logger = logging.getLogger(__name__)


def kiosk_home(request):
    return render_to_response('kiosk/home.html', {}, context_instance=RequestContext(request))


def kiosk_unknown_rfid(request):
    return render_to_response('kiosk/unknown.html', {}, context_instance=RequestContext(request))


def kiosk_associate_rfid(request):
    rfid = request.session.get('rfid', False)
    if request.method == 'POST':
        pin = request.POST.get("pin", "")
        user = activate_account_rfid(rfid, pin)
        if user:
            if user.card_uid:
                request.session['kiosk_user'] = user
                response = HttpResponse("Hello %s" % user, content_type="text/plain")
        else:
            message = """Le PIN que vous avez entré n'est pas ou n'est plus valide. Nous vous invitons à imprimer un
                      nouveau formulaire d'activation depuis le site Gelato et de recommencer la procédure. En cas
                      d'erreur répétée, veuillez vous adresser au bureau 150."""
            error = {'title': "PIN non valide", 'message': message}
            return render_to_response('kiosk/error.html', {'error': error, }, context_instance=RequestContext(request))
    else:
        return render_to_response('kiosk/associate_rfid.html', {'rfid': rfid, }, context_instance=RequestContext(request))


def kiosk_showcase(request):
    user_id = request.session.get('kiosk_user', False)
    if not user_id:
        message = """L'authentification au moyen de votre badge a échoué ou a été révoquée. Veuillez retirer et replacer
                     votre badge sur le lecteur. En cas d'erreur répétée, veuillez vous adresser au bureau 150."""
        error = {'title': "Authentification révoquée", 'message': message}
        return render_to_response('kiosk/error.html', {'error': error, }, context_instance=RequestContext(request))
    user = User.objects.get(pk=user_id)
    product_transactions = ProductTransaction.objects.all().filter(user=user).select_related('product')
    return render_to_response('kiosk/showcase.html', {'user': user, 'product_transactions': product_transactions }, context_instance=RequestContext(request))


def kiosk_error(request):
    return render_to_response('kiosk/error.html', {}, context_instance=RequestContext(request))