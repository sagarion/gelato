# -*- coding: UTF-8 -*-
# models.py
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

# Imports
import webiopi
import datetime
import memcache
import sys
sys.path.append("/home/cgaspoz/PycharmProjects/gelato/kiosk")

from celerytasks.tasks import log_kiosk

# Enable debug output
webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO

T1 = 17
T2 = 27
T3 = 22
DOOR = 23
LOCK = 24

kiosk_open = False
door_open = False
lock_open = False
lock_opened = datetime.datetime.now()
t1 = False
t2 = False
t3 = False

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.set("lock_opened", lock_opened)
mc.set("kiosk_open", kiosk_open)


# setup function is automatically called at WebIOPi startup
def setup():
    GPIO.setFunction(T1, GPIO.IN)
    GPIO.setFunction(T2, GPIO.IN)
    GPIO.setFunction(T3, GPIO.IN)
    GPIO.setFunction(DOOR, GPIO.IN)
    GPIO.setFunction(LOCK, GPIO.OUT)
    GPIO.digitalWrite(LOCK, GPIO.LOW)


# loop function is repeatedly called by WebIOPi
def loop():
    global door_open, kiosk_open, lock_open, lock_opened, t1, t2, t3
    lock_opened = mc.get("lock_opened")
    kiosk_open = mc.get("kiosk_open")
    # retrieve current datetime
    now = datetime.datetime.now()

    if GPIO.digitalRead(T1) == GPIO.LOW and t1:
        t1 = False
        # Drawer 1 closed

    if GPIO.digitalRead(T1) == GPIO.HIGH and not t1:
        t1 = True
        # Drawer 1 open

    if GPIO.digitalRead(T2) == GPIO.LOW and t2:
        t2 = False
        # Drawer 2 closed

    if GPIO.digitalRead(T2) == GPIO.HIGH and not t2:
        t2 = True
        # Drawer 2 open

    if GPIO.digitalRead(T3) == GPIO.LOW and t3:
        t3 = False
        # Drawer 3 closed

    if GPIO.digitalRead(T3) == GPIO.HIGH and not t3:
        t3 = True
        # Drawer 3 open

    if not kiosk_open:
        if GPIO.digitalRead(DOOR) == GPIO.HIGH and not door_open:
            door_open = True
            # We have an intrusion

        if GPIO.digitalRead(DOOR) == GPIO.LOW and door_open:
            door_open = False
            # Intrusion ended

    if kiosk_open:
        if GPIO.digitalRead(DOOR) == GPIO.HIGH and not door_open:
            door_open = True
            # Kiosk opened

        if GPIO.digitalRead(DOOR) == GPIO.LOW and door_open:
            door_open = False
            kiosk_open = False
            mc.set("kiosk_open", kiosk_open)
            # Kiosk closed

    if GPIO.digitalRead(LOCK) == GPIO.HIGH and lock_opened < datetime.datetime.now() - datetime.timedelta(seconds=6):
        GPIO.digitalWrite(LOCK, GPIO.LOW)
        lock_open = False

    # gives CPU some time before looping again
    webiopi.sleep(1)


# destroy function is called at WebIOPi shutdown
def destroy():
    pass
