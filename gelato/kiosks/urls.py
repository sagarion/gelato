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
from .views import kiosk_home, kiosk_unknown_rfid, kiosk_associate_rfid, kiosk_error, kiosk_showcase, kiosk_select, kiosk_exit, kiosk_sell, kiosk_check_transaction, kiosk_admin, kiosk_check_admin

urlpatterns = patterns('',
    #url(r'^rfid/(?P<rfid>\d+)/$', rfid_scan, name='rfid_scan'),
    #url(r'^summary/(?P<user_id>\d+)/$', views.summary, name='booth-summary'),
    url(r'select/(?P<product_id>\d+)/$', kiosk_select, name='kiosk_select'),
    url(r'sell/(?P<product_id>\d+)/$', kiosk_sell, name='kiosk_sell'),
    url(r'check-transaction/(?P<transaction_id>\d+)/$', kiosk_check_transaction, name='kiosk_check'),
    url(r'check-admin/(?P<user_id>\d+)/$', kiosk_check_admin, name='kiosk_check_admin'),
    url(r'error/', kiosk_error, name='kiosk_error'),
    url(r'unknown/', kiosk_unknown_rfid, name='kiosk_unknown_rfid'),
    url(r'associate/', kiosk_associate_rfid, name='kiosk_associate_rfid'),
    url(r'admin/', kiosk_admin, name='kiosk_admin'),
    url(r'showcase/', kiosk_showcase, name='kiosk_showcase'),
    url(r'exit/', kiosk_exit, name='kiosk_exit'),
    url(r'$', kiosk_home, name='kiosk_home'),
)