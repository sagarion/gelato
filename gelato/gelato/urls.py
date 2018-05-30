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

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.urls import include, path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from products.views import home
from wallets.views import cron_clean_user_pins
from django.contrib.auth import login, logout
urlpatterns = (
    # Examples:
    url(r'^p/', include('products.urls')),
    url(r'^w/', include('wallets.urls')),
    url(r'^kiosk/', include('kiosks.urls')),
    # url(r'^gelato/', include('gelato.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    #url(r'^ipn/paypal/', include('paypal.standard.ipn.urls')),
    url(r'^home/', home, name='home'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^discover/', TemplateView.as_view(template_name="discover.html"), name="discover"),
    url(r'^staff/', TemplateView.as_view(template_name="discover.html"), name="admin"),
    url(r'^cron/clean_user_pins/', cron_clean_user_pins),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^$', RedirectView.as_view(pattern_name='home')),
)

#urlpatterns += (
#    url(r'^shib/', include('shibboleth.urls')),
#)

urlpatterns = urlpatterns + tuple(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))