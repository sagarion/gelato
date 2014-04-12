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
from django.conf.urls import patterns, url

# Third-party app imports

# Gelato imports
from .views import UserListView, UserDetail, UserHomeDetail, dashboard, create_account

urlpatterns = patterns('',
    url(r'^user/(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^create_account/$', create_account, name='create_account'),
    url(r'$', UserListView.as_view(), name='users'),
)