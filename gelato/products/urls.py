# -*- coding: UTF-8 -*-
# urls.py
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
from django.conf.urls import url

# Third-party app imports

# Gelato imports
from .views import ProductListView, ProductTransactionsDetail, ProductListViewByCategory, ProductListViewByBrand

urlpatterns = (
    url(r'^product/(?P<pk>\d+)/$', ProductTransactionsDetail.as_view(), name='product_detail'),
    url(r'^category/([\w-]+)/$', ProductListViewByCategory.as_view(), name='products_by_category'),
    url(r'^brand/([\w-]+)/$', ProductListViewByBrand.as_view(), name='products_by_brand'),
    url(r'$', ProductListView.as_view(), name='products'),
)