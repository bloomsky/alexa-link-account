"""The user accounts managment"""

import requests
import json
from django.conf import settings

URL_PREFIX = settings.URL_PREFIX

class BskyUser(object):
    "The Bloomsky sky user object"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.loggedin = False
        self.token = ""
        self.warning = ""

    def login(self):
        "login as bsky user and return auth token"

        #  validate the authentication of user
        login_path = '/auth/login/'
        url_login = URL_PREFIX + login_path
        data = {"username": self.username, "password": self.password}
        headers = {'Content-type': 'application/json;charset=utf8'}
        response = requests.post(url_login, data=json.dumps(
            data, ensure_ascii=False).encode('utf8'), headers=headers)

        if response.status_code == 200:
            self.loggedin = True
            self.token = response.json()['auth_token']
        else:
            self.warning = response.json()['non_field_errors'][0]
