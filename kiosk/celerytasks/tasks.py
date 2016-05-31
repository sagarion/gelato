#!/usr/bin/python
# -*- coding: UTF-8 -*-
# tasks.py
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
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Third-party app imports
from celery import Celery
from celery.task.http import HttpDispatchTask

# Gelato imports
from products.models import Product
from kiosks.models import KioskStorage, kiosk_get_product_storage



app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def log_kiosk(kiosk, date, level, action, message):
    res = HttpDispatchTask.delay(
            url='http://example.com/multiply',
            method='GET', x=10, y=10)
    res.get()