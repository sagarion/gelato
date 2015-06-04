# -*- coding: UTF-8 -*-
# wsgi.py
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

"""
WSGI config for Gelato project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gelato.settings.production")


class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):

#        os.environ['GELATO_DATABASE_PASSWORD'] = environ['GELATO_DATABASE_PASSWORD']
#        os.environ['GELATO_SECRET_KEY'] = environ['GELATO_SECRET_KEY']
#        os.environ['GELATO_EMAIL_HOST_PASSWORD'] = environ['GELATO_EMAIL_HOST_PASSWORD']
#        os.environ['GELATO_EMAIL_HOST_USER'] = environ['GELATO_EMAIL_HOST_USER']
        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()