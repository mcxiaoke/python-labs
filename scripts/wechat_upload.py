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
from concurrent.futures import ThreadPoolExecutor

from config import WECHAT_TOKEN

UPLOAD_IMAGE_URL = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image'

def upload(ifile):
    url = UPLOAD_IMAGE_URL % WECHAT_TOKEN
    files = {'media': open(ifile, 'rb')}
    r = commons.post(url, files=files)
    return r.json()['media_id']

def main():
    media_ids = []
    list_file = upath.abspath('media_ids.txt')
    root = upath.abspath(sys.argv[1])
    for name in os.listdir(root):
        try:
            print('Uploading %s' % name)
            media_id = upload(os.path.join(root, name))
            if media_id:
                media_ids.append(media_id)
                utils.write_list(list_file, media_ids)
        except Exception as e:
            traceback.print_exc()
    utils.write_list(list_file, media_ids)

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, commons, utils, upath
    main()
