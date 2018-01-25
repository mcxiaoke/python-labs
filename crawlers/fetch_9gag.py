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
import json
import thread
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=8) 

OUTPUT = 'output-9gag'

def get_image_url(item):
    if item['type'] == 'Animated':
        return item['image460sv']['url']
    elif item['type'] == 'Photo':
        try:
            return item['image700']['url']
        except Exception as e:
            return item['image460']['url']

def download_images(items):
    if items:
        urls = [get_image_url(item) for item in items]
        urls = filter(None, urls)
        for url in urls:
            commons.download(url, OUTPUT)

def download_images_async(items):
    pool.submit(download_images, (items,))

def main():
    output = os.path.abspath(OUTPUT)
    if not os.path.exists(output):
        os.mkdir(output)
    data_file = os.path.join(output,'data_%s.json' % int(time.time()))
    root_url = 'https://9gag.com/v1/group-posts/group/gif/type/hot'
    items = []
    query_next = None
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            old_posts = utils.read_dict(sys.argv[1])
            if old_posts and len(old_posts) > 0:
                print('Old posts count=%s' % len(old_posts))
                download_images_async(old_posts)
                item = old_posts[-1]
                query_next = ('after=%s&c=10' % item['id'])
                items.extend(old_posts)
        else:
            exit(233)
    url = '%s?%s' % (root_url, query_next or '')
    r = commons.get(url)
    print('Page: %s' % url)
    while r.status_code < 300:
        posts = r.json()['data']['posts']
        items.extend(posts)
        utils.write_dict(data_file, items)
        download_images_async(items)
        query_next = r.json()['data']['nextCursor']
        if query_next:
            url = '%s?%s' % (root_url, query_next)
            print('Page: %s' % url)
            try:
                r = commons.get(url)
            except Exception as e:
                traceback.print_exc()
            


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, commons, utils
    main()