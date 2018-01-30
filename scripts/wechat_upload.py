#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-26
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import requests
import base64
import json
import sys
import os
import re
import time
import shutil
import random
import argparse
import traceback
import json
import redis
import requests
from concurrent.futures import ThreadPoolExecutor

from config import WECHAT_APPID, WECHAT_APPSECRET

MEDIA_ID_EXPIRE = 60 * 60 * 24 * 3 - 60 * 60  # in seconds
MEDIA_ID_KEY = 'wechat:media_ids:v1'
MEDIA_ID_USER_KEY = 'wechat:media_ids:v1:%s'
MEDIA_ID_FILE = 'media_ids.txt'
UPLOAD_IMAGE_URL = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image'
GET_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'

# r = redis.StrictRedis()
# r.delete(MEDIA_ID_KEY)

def get_access_token():
    url = GET_TOKEN_URL % (WECHAT_APPID, WECHAT_APPSECRET)
    r = requests.get(url)
    r.encoding = 'utf-8'
    if r.status_code < 300:
        return r.json()


def random_media_id_user(user_id):
    user_key = MEDIA_ID_USER_KEY % user_id
    mids = r.sdiff(MEDIA_ID_KEY, user_key)
    if mids:
        mid = random.choice(mids)
        r.sadd(user_key, mid)
        r.expire(user_key, MEDIA_ID_EXPIRE)
        return mid


def random_media_id():
    return r.srandmember(MEDIA_ID_KEY)

def save_media_ids(media_ids):
    # r.sadd(MEDIA_ID_KEY, media_ids)
    # r.expire(MEDIA_ID_KEY, MEDIA_ID_EXPIRE)
    with open(MEDIA_ID_FILE, 'w') as f:
        f.write('\n'.join(media_ids))


def upload_image(filepath, token):
    url = UPLOAD_IMAGE_URL % token
    files = {'media': open(filepath, 'rb')}
    try:
        r = requests.post(url, files=files)
        r.encoding = 'utf-8'
        return r.json()['media_id']
    except Exception as e:
        traceback.print_exc()
        # raise e


def upload_images(root, token, max_count=300):
    mids = []
    names = os.listdir(root)[:max_count]
    count = 0
    for name in os.listdir(root):
        filepath = os.path.join(root, name)
        print('Uploading image: %s' % filepath)
        media_id = upload_image(filepath, token)
        if media_id:
            print('Uploaded image: %s' % media_id)
            mids.append(media_id)
            save_media_ids(mids)
        count += 1
        if count > max_count:
            break
    mids = filter(None, mids)
    save_media_ids(mids)
    return mids


def main():
    try:
        from config import WECHAT_TOKEN as token_json
        token_json = json.loads(token_json)
    except Exception as e:
        token_json = get_access_token()
    print(token_json)
    if token_json:
        token = token_json['access_token']
        upload_images(sys.argv[1], token)


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    main()

