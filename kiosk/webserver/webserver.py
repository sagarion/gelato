import web  # requires web.py
import requests
import json

urls = (
    '/open/(.+)/', 'open',
)

LOGIN = "http://localhost:8000/accounts/login/"
URL = "http://localhost:8000/kiosk/check-transaction/"
USERNAME = 'gelato1'
PASSWORD = 'gelato1'


def check_transaction(transaction):
    client = requests.session()
    # Retrieve the CSRF token first
    client.get(LOGIN)  # sets the cookie
    csrftoken = client.cookies['csrftoken']
    data = dict(username=USERNAME, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next=URL + transaction + '/')
    r = client.post(LOGIN, data=data, headers={"Referer": "Gelato Kiosk"})
    confirmation = json.loads(r.content)
    if confirmation['success']:
        return True
    else:
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
            # TODO: open the kiosk
            return {'success': True, 'message': u"La porte est ouverte"}
        else:
            return {'success': False, 'message': u"La porte n'a pas pu &ecirc;tre ouverte"}


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()