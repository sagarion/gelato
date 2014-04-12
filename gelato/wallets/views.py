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

# Core Django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Sum
#from django.contrib.auth.models import User
from django.conf import settings

# Third-party app imports

# Gelato imports
from transactions.models import ProductTransaction, FinancialTransaction
from .models import User


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
    if user.is_active == 0:
        HttpResponseRedirect('create_account')

    financial_transactions = FinancialTransaction.objects.all().filter(user=user)
    product_transactions = ProductTransaction.objects.all().filter(user=user)
    return render_to_response('wallets/dashboard.html', {"financial_transactions": financial_transactions,
                                                         "product_transactions": product_transactions,
                                                         "user": user, }, context_instance=RequestContext(request))


@login_required()
def create_account(request):
    user = request.user
    if user.is_active == 1:
        HttpResponseRedirect('dashboard')

    return render_to_response('wallets/create_account.html', {"user": user, }, context_instance=RequestContext(request))


class UserHomeDetail(TemplateView):
    template_name = "wallets/home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserHomeDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserHomeDetail, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context