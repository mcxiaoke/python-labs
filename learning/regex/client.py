# -*- coding: utf-8 -*-

from pyoauth2 import Client
from pyoauth2 import AccessToken
import os


class ApiClient:
    API_HOST = 'https://api.douban.com'
    AUTH_HOST = 'https://www.douban.com'
    TOKEN_URL = AUTH_HOST + '/service/auth2/token'
    AUTHORIZE_URL = AUTH_HOST + '/service/auth2/auth'
    ACCESS_TOKEN_FILE = "data/access_token.txt"
    DEFAULT_START = 0
    DEFAULT_COUNT = 20

    def __init__(self, key, secret, redirect='', scope=''):
        self.redirect_uri = redirect
        self.scope = scope
        self.client = Client(key, secret,
                             site=self.API_HOST,
                             authorize_url=self.AUTHORIZE_URL,
                             token_url=self.TOKEN_URL)
        self.access_token = AccessToken(self.client, '')
        self.load_token()

    def __repr__(self):
        return '<ApiClient OAuth2>'


    def auth_with_code(self, code):
        self.access_token = self.client.auth_code.get_token(code, redirect_uri=self.redirect_uri)

    def auth_with_token(self, token):
        self.access_token = AccessToken(self.client, token)

    def auth_with_password(self, username, password, **opt):
        self.access_token = self.client.password.get_token(username=username, password=password,
                                                           redirect_uri=self.redirect_uri, **opt)

    def refresh_token(self, refresh_token):
        access_token = AccessToken(self.client, token='', refresh_token=refresh_token)
        self.access_token = access_token.refresh()

    def me(self):
        return self.access_token.get("/v2/lifestream/user/~me")

    def user(self, id):
        return self.access_token.get("/v2/lifestream/user/%d" % id)

    def followings(self, id, count=DEFAULT_COUNT, start=DEFAULT_START):
        return self.access_token.get("/v2/lifestream/user/%d/followings" % id, count=count, start=start)

    def followers(self, id, count=DEFAULT_COUNT, start=DEFAULT_START):
        return self.access_token.get("/v2/lifestream/user/%d/followers" % id, count=count, start=start)

    @property
    def authorize_url(self):
        return self.client.auth_code.authorize_url(redirect_uri=self.redirect_uri, scope=self.scope)

    @property
    def token_code(self):
        return self.access_token and self.access_token.token

    @property
    def refresh_token_code(self):
        return getattr(self.access_token, 'refresh_token', None)


    def save_token(self):
        print "save_token:", self.token_code
        with open(self.ACCESS_TOKEN_FILE, "w") as f:
            f.write(self.token_code)
            f.flush()

    def load_token(self):
        if os.path.isfile(self.ACCESS_TOKEN_FILE):
            f = open(self.ACCESS_TOKEN_FILE, "r")
            self.access_token.token = f.read()
            print "load_token:", self.token_code
