# -*- coding: UTF-8 -*-
# admin.py
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
from django.contrib import admin

# Third-party app imports

# Gelato imports
from .models import User, UserPin


class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'card_uid', 'is_active')


class UserPinAdmin(admin.ModelAdmin):
    list_display = ('user', 'pin', 'pin_creation')


admin.site.register(User, UserAdmin)
admin.site.register(UserPin, UserPinAdmin)