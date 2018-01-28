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
import thread
import redis
import requests
from concurrent.futures import ThreadPoolExecutor

from config import WECHAT_TOKEN

MEDIA_ID_EXPIRE = 60*60*24*3 - 60*60 # in seconds
MEDIA_ID_KEY = 'wechat:media_ids:v1'
MEDIA_ID_USER_KEY = 'wechat:media_ids:v1:%s'
MEDIA_ID_FILE = 'media_ids.txt'
UPLOAD_IMAGE_URL = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image'

r = redis.StrictRedis()

def random_media_id_user(user_id):
    user_key = MEDIA_ID_USER_KEY % user_id
    mids = r.sdiff(MEDIA_ID_KEY, user_key)
    if mids:
        mid = random.choice(ids)
        r.sadd(user_key, mid)
        r.expire(user_key, MEDIA_ID_EXPIRE)
        return mid

def random_media_id():
    return r.srandmember(MEDIA_ID_KEY)

def save_media_ids(*media_ids):
    r.sadd(MEDIA_ID_KEY, media_ids)
    r.expire(MEDIA_ID_KEY, MEDIA_ID_EXPIRE)
    with open(MEDIA_ID_FILE, 'wb') as f:
        f.write(','.join(media_ids))

def upload_image(ifile):
    url = UPLOAD_IMAGE_URL % WECHAT_TOKEN
    files = {'media': open(ifile, 'rb')}
    try:
        r = requests.post(url, files=files)
        return r.json()['media_id']
    except Exception as e:
        return None

def upload_images(idir, max_count=100):
    mids = []
    names = os.listdir(root)[:max_count]
    for name in os.listdir(idir):
        ipath = os.path.join(idir, name)
        mid = upload_image(ifile)
        if mid:
            mids.extend(mid)
    mids = filter(None, mids)
    save_media_ids(mids)
    return mids

def main():
    upload_images(sys.argv[1])

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, commons, utils, upath
    main()
