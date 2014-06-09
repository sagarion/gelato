# -*- coding: UTF-8 -*-
# gelato-kiosk-webserver.py
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


import web  # requires web.py
import requests
import json
import logging


urls = (
    '/open/(.+)/', 'open',
)

LOGIN = "http://marmix.ig.he-arc.ch/gelato/accounts/login/"
URL = "http://marmix.ig.he-arc.ch/gelato/kiosk/check-transaction/"
USERNAME = 'gelato1'
PASSWORD = 'gelato7cold'

logger = logging.getLogger("Kiosk Webserver")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/gelato/kiosk-webserver.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_transaction(transaction):
    logger.info("Check transaction: %s" % transaction)
    client = requests.session()
    # Retrieve the CSRF token first
    client.get(LOGIN)  # sets the cookie
    csrftoken = client.cookies['csrftoken']
    data = dict(username=USERNAME, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next=URL + transaction + '/')
    r = client.post(LOGIN, data=data, headers={"Referer": "Gelato Kiosk"})
    confirmation = json.loads(r.content)
    if confirmation['success']:
        logger.info("Check succeed: %s" % confirmation['message'])
        return True
    else:
        logger.info("Check failed: %s" % confirmation['message'])
        return False


class open:
    def GET(self, transaction):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        transaction = transaction
        # We check if we have a valid transaction
        confirmation = check_transaction(transaction)
        if confirmation:
            # We open the kiosk and return a confirmation message
            return {'success': True, 'message': u"La porte est ouverte"}
        else:
            return {'success': False, 'message': u"La porte n'a pas pu être ouverte"}


if __name__ == "__main__":
    app = web.application(urls, globals())
    logger.info("Starting the Kiosk Webserver daemon...")
    app.run()

logger.info("Terminating the Kiosk Webserver daemon...")