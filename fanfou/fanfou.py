#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 07:26:59

import requests
from requests_oauthlib import OAuth1
from xauth import AuthClient
import config


class FanfouError(Exception):

    def __init__(self, response):
        self.response = response

# https://github.com/FanfouAPI/FanFouAPIDoc/wiki/Apicategory
# date time format --> Wed Aug 05 12:59:18 +0000 2015


class FanfouClient:

    def __init__(self, oauth_token=None):
        self.consumer_key = config.CONSUMER_KEY
        self.consumer_secret = config.CONSUMER_SECRET
        self.token_url = config.TOKEN_URL
        self.api_host = config.API_HOST
        self.oauth_token = None
        self.user = None
        self._check_auth(oauth_token)

    def _get_url(self, path):
        return self.api_host+path+".json"

    def _check_auth(self, oauth_token):
        if oauth_token:
            self.oauth_token = oauth_token
            self.oauth = OAuth1(self.consumer_key,
                                client_secret=self.consumer_secret,
                                resource_owner_key=oauth_token["oauth_token"],
                                resource_owner_secret=oauth_token[
                                    "oauth_token_secret"],
                                signature_type='auth_header')
            self.user = self.verify_credentials()
            return self.user

    def _send_request(self, method, path, **kwargs):
        print "[request] %s %s %s" % (method, path, kwargs)
        url = self._get_url(path)
        try:
            r = requests.request(method, url, auth=self.oauth, **kwargs)
            #print "[response]", r.url, r.status_code, r.encoding
            if r.status_code >= requests.codes.ok and r.status_code < 400:
                return r.json()
            else:
                raise FanfouError(r)
        except requests.RequestException, e:
            print e

    def set_oauth_token(self, oauth_token):
        self._check_auth(oauth_token)

    def is_verified(self):
        return self.oauth_token and self.user

    def get(self, path, **kwargs):
        return self._send_request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self._send_request("POST", path, **kwargs)

    def delete(self, path, **kwargs):
        return self._send_request("DELETE", path, **kwargs)

    def put(self, path, **kwargs):
        return self._send_request("PUT", path, **kwargs)

    def login(self, username, password):
        client = AuthClient(
            self.consumer_key, self.consumer_secret, self.token_url)
        access_token = client.get_access_token(username, password)
        print "login successful, token is", access_token
        self._check_auth(access_token)
        return access_token

    def get_rate_limit_status(self):
        return self.get("/account/rate_limit_status")

    def search_public_timeline2(self, keyword, count=0,
                                since_id=None, max_id=None, mode=None):
        params = {"q": keyword, "since_id": since_id,
                  "max_id": max_id, "count": count,
                  "mode": mode, "format": "html"}
        return self.get("/search/public_timeline", params=params)

    def search_public_timeline(self, keyword, **kwargs):
        params = kwargs if kwargs else {}
        params["q"] = keyword
        return self.get("/search/public_timeline", params=params)

    def search_user_timeline(self, keyword, user_id, **kwargs):
        params = kwargs if kwargs else {}
        params["q"] = keyword
        params['id'] = user_id
        return self.get("/search/user_timeline", params=params)

    def get_home_timeline(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("/statuses/home_timeline", params=params)

    def get_public_timeline(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("/statuses/public_timeline", params=params)

    def get_mentions(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("/statuses/mentions", params=params)

    def get_user_timeline(self, user_id, **kwargs):
        params = kwargs if kwargs else {}
        params['id'] = user_id
        return self.get("/statuses/user_timeline", params=params)

    def get_user_photos(self, user_id, **kwargs):
        params = kwargs if kwargs else {}
        params['id'] = user_id
        return self.get("/photos/user_timeline", params=params)

    def get_user_favorites(self, user_id, **kwargs):
        params = kwargs if kwargs else {}
        #params['id'] = user_id
        return self.get("/favorites/%s" % user_id, params=params)

    def get_context_timeline(self, status_id, **kwargs):
        params = kwargs if kwargs else {}
        params['id'] = status_id
        return self.get("/statuses/context_timeline", params=params)

    def get_status(self, status_id, **kwargs):
        params = kwargs if kwargs else {}
        params['id'] = status_id
        return self.get("/statuses/show", params=params)

    def get_inbox_messages(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("/direct_messages/inbox", kwargs)

    def get_outbox_messages(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("//direct_messages/sent", kwargs)

    def get_conversation_list(self, **kwargs):
        params = kwargs if kwargs else {}
        return self.get("/privete_messages/conversation_list", kwargs)

    def get_conversation(self, user_id, **kwargs):
        params = kwargs if kwargs else {}
        params['id'] = user_id
        return self.get("/privete_messages/conversation_list", kwargs)

    def get_trends(self):
        return self.get("/photos/user_timeline",)

    def search_user(self, keyword, **kwargs):
        params = kwargs if kwargs else {}
        params["q"] = keyword
        return self.get("/search/users", params=params)

    def verify_credentials(self):
        return self.get("/account/verify_credentials")

    def get_user(self, user_id, **kwargs):
        params = kwargs if kwargs else {}
        params["id"] = user_id
        return self.get("/users/show", params=params)

    def get_followers(self, user_id=None, **kwargs):
        params = kwargs if kwargs else {}
        params["id"] = user_id
        return self.get("/users/followers", params=params)

    def get_friends(self, user_id=None, **kwargs):
        params = kwargs if kwargs else {}
        params["id"] = user_id
        return self.get("/users/friends", params=params)

    def update_profile(self, **kwargs):
        data = kwargs if kwargs else {}
        return self.post("/account/update_profile", data=data)

    def post_status(self, status):
        data = kwargs if kwargs else {}
        data['status'] = status
        return self.post("/account/update_profile", data=data)

if __name__ == '__main__':
    client = FanfouClient()
    client.login("test", "test")
    client.verify_credentials()
    #client.get_home_timeline(count=1)
    #user = client.get_user("wangxing", mode="default", format="html")
    #timeline = client.get_user_timeline("blessedkristin", count=1)
