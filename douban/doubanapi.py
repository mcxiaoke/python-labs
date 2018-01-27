#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-26 12:35:52
from __future__ import print_function
import requests
import base64
import json
import sys
import os
import codecs

TOKEN_FILENAME = '.douban.token.dat'
AUTH_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
API_DOMAIN = 'https://api.douban.com/v2'

DFD_EDOMAIN = 'aHR0cHM6Ly9mcm9kby5kb3ViYW4uY29tL2FwaS92Mg=='
DFD_EKEY = 'MDdjNzg3ODJkYjAwYTEyMTE3NTY5Njg4OTEwMWUzNjM='
DFD_ESECRET = 'OTgxZGE5YjA5ODg3ZjEzZg=='
DFD_REDIRECT = 'aHR0cHM6Ly93d3cuZG91YmFuLmNvbS9hY2NvdW50cy9hdXRoMl9yZWRpcj91cmw9aHR0cDovL3NodW8uZG91YmFuLmNvbS8hc2VydmljZS9hbmRyb2lkJmFwaWtleT0gMDdjNzg3ODJkYjAwYTEyMTE3NTY5Njg4OTEwMWUzNjM='
DFD_EUA_FRODO = 'YXBpLWNsaWVudC8xIGNvbS5kb3ViYW4uZnJvZG8vNS4xOC4wLjAoOTgpIEFuZHJvaWQvMjEgY2FuY3JvX3djX2x0ZSBYaWFvbWkgTUkgNFcgIHJvbTptaXVpNg=='
DFD_EUA_SHUO = 'YXBpLWNsaWVudC8yLjMuMCBjb20uZG91YmFuLnNodW8vMi4yLjUoMTIxKSBBbmRyb2lkLzIxIGNhbmNyb193Y19sdGUgWGlhb21pIE1JIDRX'
UDID = '593d6cbdb087edc6ab268d38e96d1b94b44b8d72'

def write_dict(name, dt):
    if not dt:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        json.dump(dt, f)


def read_dict(name):
    if not os.path.isfile(name):
        return {}
    with codecs.open(name, 'r', 'utf-8') as f:
        return json.load(f)

def request_to_curl(r):
    req = r.request
    method = req.method
    uri = req.url
    ct = req.headers.get('Content-Type')
    data = '[multipart]' if ct and 'multipart/form-data' in ct else (
        req.body or '')
    headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    return command.format(method=method, headers=headers, data=data, uri=uri)

def need_login(func):
    def wrapper(*args, **kwargs):
        #print('args - ',args)
        #print('kwargs - ',kwargs)
        obj = args[0]
        if not obj.is_authorized():
            print("method '%s' need login!" % func.__name__)
            obj.check_login()
        if not obj.is_authorized():
            print("method '%s' need login, abort!" % func.__name__)
            exit(233)
        return func(*args, **kwargs)

    return wrapper


class ApiClient(object):

    def __init__(self, host=API_DOMAIN,
                 key=base64.b64decode(DFD_EKEY),
                 secret=base64.b64decode(DFD_ESECRET),
                 token_file=TOKEN_FILENAME):
        self.debug = False
        self.host = host
        self.key = key
        self.secret = secret
        self.token_file = token_file
        self.redirect_uri = base64.b64decode(DFD_REDIRECT)
        self.ua = base64.b64decode(DFD_EUA_SHUO)
        self.udid = UDID
        self.id = None
        self.tk = None
        self._read_token()
        # print('ApiClient() host={}, apikey={}, udid={}, ua={}'
        #       .format(self.host, self.key, self.udid, self.ua))
        if self.is_authorized():
            self._log_print('ApiClient(%s, %s)' % (self.id, self.tk))
        else:
            self._log_print('ApiClient()')

    def _read_token(self):
        if os.path.exists(self.token_file):
            res = read_dict(self.token_file)
            if res:
                self.id = res.get('douban_user_id')
                self.tk = res.get('access_token')
                return self.is_authorized()

    def _write_token(self, res):
        if self.is_authorized() and res:
            write_dict(self.token_file, res)
            return True

    def check_login(self):
        if not self.is_authorized():
            try:
                from config import USERNAME, PASSWORD
            except Exception as e:
                USERNAME = None
                PASSWORD = None
            username = USERNAME or input('Username: ')
            password = PASSWORD or input('Password: ')
            if username and password:
                print('login using %s:%s' % (username, password))
                self.login(username, password)
            if self.is_authorized():
                print('login successful, continue.')
            else:
                print('login failed, abort.')
                exit(2)
        else:
            print('already logged in.')

    def logout(self):
        self.id = None
        self.tk = None
        if os.path.exists(self.token_file):
            os.remove(self.token_file)

    def _log_print(self, message):
        if self.debug:
            print(message)

    def log_request(self, r):
        self._log_print('[Request] {}'.format(request_to_curl(r)))
        self._log_print('[Response] {} {} ({}:{})'.
                        format(r.request.method, r.url, r.status_code, r.reason))

    def _get_url(self, url, params=None, **options):
        headers = {
            'User-Agent': self.ua
        }
        if self.is_authorized():
            headers['Authorization'] = 'Bearer {0}'.format(self.tk)
        if not params:
            params = {}
        params['apikey'] = self.key
        params['udid'] = self.udid
        r = requests.get(url, params=params, headers=headers, **options)
        self.log_request(r)
        if r.status_code >= 400:
            print(r.text)
        return r.json()

    def _post_url(self, url, params=None, **options):
        headers = {
            'User-Agent': self.ua
        }
        if self.is_authorized():
            headers['Authorization'] = 'Bearer {0}'.format(self.tk)
        if not params:
            params = {}
        params['apikey'] = self.key
        params['udid'] = self.udid
        r = requests.post(url,
                          params=params, headers=headers, **options)
        self.log_request(r)
        if r.status_code >= 400:
            print(r.text)
        return r.json()

    def _get(self, path, params=None, **options):
        return self._get_url(self.host + path, params, **options)

    def _post(self, path, params=None, **options):
        return self._post_url(self.host + path, params, **options)

    def is_authorized(self):
        return self.id and self.tk

    def login(self, username, password):
        data = {
            'client_id': self.key,
            'client_secret': self.secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        res = self._post_url(AUTH_TOKEN_URL, data=data)
        if res:
            self.id = res.get('douban_user_id')
            self.tk = res.get('access_token')
            self._write_token(res)

    @need_login
    def me(self):
        return self._get('/user/~me')

    def album_info(self, id):
        # GET /photo_album/:id
        return self._get('/photo_album/%s' % id)

    @need_login
    def album_like(self, id):
        # POST/photo_album/:id/like
        return self._post('/photo_album/%s/like' % id)

    @need_login
    def album_unlike(self, id):
        # POST /photo_album/:id/unlike
        return self._post('/photo_album/%s/unlike' % id)

    def album_photos(self, id, start=0, count=20):
        # GET /photo_album/:id/photos?start=&count=
        params = {'start': start, 'count': count}
        return self._get('/photo_album/%s/photos' % id, params)

    def user_albums(self, id, start=0, count=20):
        # GET /user/:id/photo_albums?start=&count=
        params = {'start': start, 'count': count}
        return self._get('/user/%s/photo_albums' % id, params)

    def user_notes(self, id, start=0, count=20):
        # GET /user/:id/notes?start=&count=
        params = {'start': start, 'count': count}
        return self._get('/user/%s/notes' % id, params)

    @need_login
    def user_likes(self, id, cat, start=0, count=20):
        # GET /v2/user/:id/likes
        # cat ’all’, ‘note’, ‘photo_album’, ‘photo’, ‘online’, ‘topic’, ‘experience’, ‘dongxi’
        params = {'cat': cat, 'start': start, 'count': count}
        return self._get('/user/%s/likes' % id, params)

    def user_items(self, id):
        # GET /v2/user/:id/itemlist
        return self._get('/user/%s/itemlist' % id)

    def user_collect(self, id, type, start=0, count=20):
        # GET /v2/user/:id/collect_items
        # start,count,type  ‘movie’, ‘book’, ‘music’, ‘game’, ‘app’
        params = {'type': type, 'start': start, 'count': count}
        return self._get('/user/%s/collect_items' % id, params=params)

    def user_info(self, id):
        return self._get('/user/%s' % id)

    @need_login
    def user_follow(self, id):
        # POST /v2/user/:id/follow
        return self._post('/user/%s/follow' % id)

    @need_login
    def user_unfollow(self, id):
        # POST /v2/user/:id/unfollow
        return self._post('/user/%s/unfollow' % id)

    def user_followings(self, id, start=0, count=20):
        # GET /v2/user/:id/following
        params = {'start': start, 'count': count}
        return self._get('/user/%s/following' % id, params=params)

    def user_followers(self, id, start=0, count=20):
        # GET /v2/user/:id/followers
        params = {'start': start, 'count': count}
        return self._get('/user/%s/followers' % id, params=params)

    def user_timeline(self, id, since_id=None, max_id=None):
        # GET /lifestream/user_timeline/
        params = {'since_id': since_id, 'max_id': max_id}
        r = self._get('/lifestream/user_timeline/%s' % s, params=params)
        return r.json()

    def movie_info(self, id):
        # GET /v2/movie/:id
        return self._get('/movie/%s' % id)

    def tv_info(self, id):
        # GET /v2/tv/:id
        return self._get('/tv/%s' % id)

    def book_info(self, id):
        # GET /v2/book/:id
        return self._get('/book/%s' % id)

    def music_info(self, id):
        # GET /v2/music/:id
        return self._get('/music/%s' % id)

    def doulist_info(self, id):
        # GET /v2/doulist/:name
        return self._get('/doulist/%s' % id)

    def doulist_items(self, id):
        # GET /v2/doulist/:name/items start count
        return self._get('/doulist/%s/items' % id)

    @need_login
    def doulist_add(self, id, foreign_type, foreign_item_id, comment=None):
        # POST /v2/doulist/:id/add_item
        # foreign_type
        # foreign_item_id
        # comment
        payload = {'foreign_type': foreign_type,
                   'foreign_item_id': foreign_item_id,
                   'comment': comment}
        return self._post('/doulist/%s/add_item' % id, data=payload)

    @need_login
    def doulist_follow(self, id):
        # POST /v2/doulist/:name/follow
        return self._post('/doulist/%s/follow' % id)

    @need_login
    def doulist_unfollow(self, id):
        # POST /v2/doulist/:name/unfollow
        return self._post('/doulist/%s/unfollow' % id)

    @need_login
    def doulist_create(self, title, desc=None, tags=None):
        # POST /v2/doulist/create
        # title, desc, tags
        payload = {'title': title, 'desc': desc, 'tags': tags}
        return self._post('/doulist/create', data=payload)

    def group_info(self, id):
        # GET /v2/group/:id
        return self._get('/group/%s' % id)

    def group_topics(self, id):
        # GET /v2/group/:id/topics
        return self._get('/group/%s/topics' % id)

    def group_topic(self, id):
        # GET /v2/group/topic/:id
        return self._get('/group/topic/%s' % id)

    def group_topic_comments(self, id):
        # GET /v2/group/topic/:id/comments
        return self._get('/group/topic/%s/comments' % id)

    @need_login
    def photo_upload(self, id, image, desc=None):
        # POST /v2/album/:id
        # image = photo
        files = {'image': open(image, 'rb')}
        payload = {'desc': desc or image}
        return self._post('/album/%s' % id, data=payload, files=files)


if __name__ == '__main__':
    api = ApiClient()
    if api.is_authorized():
        print(api.me())
    else:
        print(api.user_info('1000001'))
