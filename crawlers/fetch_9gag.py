#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-25
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
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.ERROR)

pool = ThreadPoolExecutor(max_workers=8) 

OUTPUT = 'output-9gag'

def get_image_url(item):
    if item['type'] == 'Animated':
        return item['images']['image460sv']['url']
    elif item['type'] == 'Photo':
        try:
            return item['images']['image700']['url']
        except Exception as e:
            traceback.print_exc()

def download_images(items):
    if items:
        urls = filter(None, [get_image_url(item) for item in items])
        for url in urls:
            print('Downloading: %s' % url)
            download_file(url, output=OUTPUT)

def download_images_async(items):
    pool.submit(download_images, items)

def main():
    output = os.path.abspath(OUTPUT)
    if not os.path.exists(output):
        os.mkdir(output)
    data_file = os.path.join(output,'data_%s.json' % int(time.time()))
    # root_url = 'https://9gag.com/v1/group-posts/group/gif/type/hot'
    # root_url = 'https://9gag.com/v1/group-posts/group/cute/type/hot'
    root_url = 'https://9gag.com/v1/group-posts/group/comic/type/hot'
    items = []
    query_next = None
    url = '%s?%s' % (root_url, query_next or '')
    r = get(url)
    print('Page: %s' % url)
    while r.status_code < 300:
        posts = r.json()['data']['posts']
        if not posts:
            break
        items.extend(posts)
        utils.write_dict(data_file, items)
        download_images_async(posts)
        query_next = r.json()['data']['nextCursor']
        if query_next:
            url = '%s?%s' % (root_url, query_next)
            print('Page: %s' % url)
            try:
                r = get(url)
            except Exception as e:
                traceback.print_exc()
            


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import utils
    from lib.compat import json
    from lib.commons import download_file, get
    main()