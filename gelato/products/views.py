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
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.db.models import Sum
from django.db import connection

# Third-party app imports

# Gelato imports
from .models import Product, ProductCategory, ProductBrand
from transactions.models import ProductTransaction


class ProductListView(ListView):
    model = Product
    # TODO: Filter products with stock > 0


class ProductTransactionsDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductTransactionsDetail, self).get_context_data(**kwargs)
        context['transaction_list'] = ProductTransaction.objects.all().filter(product=self.object)
        qty_sold = ProductTransaction.objects.all().filter(product=self.object).filter(product_transaction_type=ProductTransaction.SALE).aggregate(Sum('quantity'))['quantity__sum']
        if not qty_sold:
            context['quantity_sold'] = 0
        else:
            context['quantity_sold'] = qty_sold * -1
        return context


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def bestsellers():
    cursor = connection.cursor()
    cursor.execute("SELECT p.k_name as name, p.k_picture as img_url, SUM(t.quantity) as quantity \
                    FROM transactions_producttransaction t, products_product p \
                    WHERE t.product_id = p.id \
                    GROUP BY p.id \
                    ORDER BY quantity DESC \
                    LIMIT 5")
    rows = dictfetchall(cursor)

    return rows


def home(request):
    brands = ProductBrand.objects.all()
    sales = bestsellers()
    return render_to_response('home.html', {"brands": brands, "sales": sales}, context_instance=RequestContext(request))