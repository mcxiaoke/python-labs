#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-26
from __future__ import print_function, unicode_literals, absolute_import
import json
import sys
import os
import re
import time
import shutil
import random
import traceback
import json
import redis
import requests
import logging
import requests

TYPE_CAT = 'cats'
TYPE_DOG = 'dogs'
TYPE_OTHER = 'others'
SOURCE_ROOT = os.path.join('..', 'images')

TWO_HOUR_EXPIRE = 60*60*2  # in seconds
MEDIA_ID_EXPIRE = TWO_HOUR_EXPIRE * 35  # in seconds
ACCESS_TOKEN_KEY = 'wechat:token:v1:%s'
MEDIA_ID_KEY = 'wechat:media_ids:v1:%s'
MEDIA_ID_USER_KEY = 'wechat:media_ids:v1:%s:%s'
MEDIA_ID_FILE = 'media_ids_v1_%s.txt'
UPLOAD_IMAGE_URL = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image'
GET_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('MediaCache')
_redis = redis.StrictRedis(decode_responses=True)


def get_wechat_access_token(app_id, app_secret):
    url = GET_TOKEN_URL % (app_id, app_secret)
    logger.info('get_wechat_access_token url=%s' % url)
    response = requests.get(url)
    response.encoding = 'utf-8'
    logger.info('get_wechat_access_token result=%s' % response.json())
    return response.json()['access_token']


class MediaCache(object):

    def __init__(self, name, app_id, app_secret, r=_redis, expire=MEDIA_ID_EXPIRE):
        assert name, 'name  can not be None'
        assert app_id, 'app_id can not be None'
        assert app_secret, 'app_secret can not be None'
        self.name = name
        self.app_id = app_id
        self.app_secret = app_secret
        self.expire = expire
        self.r = r
        logger.info('__init__ name=%s app_id=%s, app_secret=%s' %
                    (name, app_id, app_secret))

    def _get_media_key(self, type_name=''):
        return MEDIA_ID_KEY % type_name

    def _get_media_file(self, type_name=''):
        return MEDIA_ID_FILE % type_name

    def _get_user_key(self, user_id, type_name=''):
        return MEDIA_ID_USER_KEY % (type_name, user_id)

    def _get_access_token(self):
        token = self.r.get(ACCESS_TOKEN_KEY % self.app_id)
        if not token:
            token = get_wechat_access_token(self.app_id, self.app_secret)
            logger.info('get_wechat_access_token token=%s' % token)
            if token:
                self.r.set(ACCESS_TOKEN_KEY % self.app_id, token)
                self.r.expire(ACCESS_TOKEN_KEY % self.app_id, TWO_HOUR_EXPIRE)
        return token

    def clear_media_ids(self, type_name=''):
        logger.info('clear_media_ids type=%s' % type_name)
        self.r.delete(self._get_media_key(type_name))

    def save_media_ids(self, media_ids, type_name='', replace=True):
        if media_ids:
            with open(self._get_media_file(type_name), 'w') as f:
                f.write('\n'.join(media_ids))
            key = self._get_media_key(type_name)
            if replace:
                self.r.delete(key)
            self.r.sadd(key, *media_ids)
            self.r.expire(key, self.expire)
            logger.info('save_media_ids %s media ids saved' % len(media_ids))
            return media_ids

    def upload_image(self, filepath):
        token = self._get_access_token()
        if not token:
            raise IOError('token is None')
        url = UPLOAD_IMAGE_URL % token
        files = {'media': open(filepath, 'rb')}
        try:
            response = requests.post(url, files=files)
            response.encoding = 'utf-8'
            return response.json()['media_id']
        except Exception as e:
            logger.error('upload_image error=%s' % e)

    def upload_images(self, source_dir, type_name='', max_count=100):
        if not source_dir or not os.path.isdir(source_dir):
            return
        names=os.listdir(source_dir)[:max_count]
        count=0
        mids=[]
        for name in names:
            filepath=os.path.join(source_dir, name)
            filepath=os.path.abspath(filepath)
            if not name.lower().endswith('.jpg'):
                logger.warning('upload_images invalid=%s' % filepath)
                continue
            logger.info('upload_images file=%s' % filepath)
            media_id=self.upload_image(filepath)
            if media_id:
                logger.info('upload_images result=%s' % media_id)
                mids.append(media_id)
            count += 1
            if count > max_count:
                break
        self.save_media_ids(mids)

    def random_user_media_id(self, user_id, type_name=''):
        media_key=self._get_media_key(type_name)
        user_key=self._get_user_key(user_id, type_name)
        mids=self.r.sdiff(media_key, user_key)
        if mids:
            mid=random.choice(list(mids))
            if mid:
                self.r.sadd(user_key, mid)
                self.r.expire(user_key, self.expire)
        else:
            self.r.delete(user_key)
            mid = self.random_media_id()
        logger.info('random_user_media_id result=%s' % mid)
        return mid

    def all_media_ids(self, type_name=''):
        return self.r.smembers(self._get_media_key(type_name))

    def media_ids_length(self, type_name=''):
        return self.r.scard(self._get_media_key(type_name))

    def random_media_id(self, type_name=''):
        return self.r.srandmember(self._get_media_key(type_name))


from config import WECHAT_APPID, WECHAT_APPSECRET, WECHAT2_APPID, WECHAT2_APPSECRET

cache1=MediaCache('Cat', WECHAT_APPID, WECHAT_APPSECRET)
cache2=MediaCache('Miu', WECHAT2_APPID, WECHAT2_APPSECRET)

def update_app(cache, root=SOURCE_ROOT):
    for type_name in (TYPE_CAT, TYPE_DOG, TYPE_OTHER):
        source_dir=os.path.join(root, type_name)
        cache.upload_images(source_dir, type_name)

def update_all(root=SOURCE_ROOT):
    update_app(cache1, root)
    update_app(cache2, root)

def check_all(root=SOURCE_ROOT):
    for type_name in (TYPE_CAT, TYPE_DOG, TYPE_OTHER):
        source_dir=os.path.join(root)
        source_dir=os.path.abspath(source_dir)
        if not os.path.exists(source_dir):
            print('source dir [%s] not exists' % source_dir)
            exit(1)
        if not os.path.isdir(source_dir):
            print('source dir [%s] not directory' % source_dir)
            exit(2)
        if not os.listdir(source_dir):
            print('source dir [%s] is empty' % source_dir)
            exit(2)

def test():
    cache1.random_user_media_id('a')
    cache1.random_user_media_id('a')
    cache1.random_user_media_id('a')
    cache2.random_user_media_id('a')
    cache2.random_user_media_id('a')
    cache2.random_user_media_id('a')


if __name__ == '__main__':
        # check_all(sys.argv[1])
        # update_all(sys.argv[1])
        test()
