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
import traceback
import json
import requests
from lxml import etree

sys.path.insert(1, os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
from lib import commons, utils
from lib.compat import text_type, binary_type, to_text, to_binary

OUTPUT = '../lib/proxies.txt'

# proxy list https://pastebin.mozilla.org/?dl=9076632

def swei360():
    url = 'http://www.swei360.com/free/?stype=1&page=1'
    r = commons.get(url)
    t = to_text(r.text)
    tree = etree.HTML(t)
    ps = tree.xpath('//*[@id="list"]/table/tbody/tr')
    for p in ps:
        px = ':'.join(p.xpath('./td/text()')[0:2])
        print(px)

def ip3366():
    url = 'http://www.ip3366.net/free/?stype=1&page=1'
    r = commons.get(url)
    t = to_text(r.text)
    tree = etree.HTML(t)
    ps = tree.xpath('//*[@id="list"]/table/tbody/tr')
    for p in ps:
        px = ':'.join(p.xpath('./td/text()')[0:2])
        print(px)

def main():
    text = commons.get('https://pastebin.mozilla.org/?dl=9076632').text
    proxy_list = [p.strip() for p in text.split('\n')]
    for p in proxy_list:
        proxies = {
            "http": "http://%s" % p,
            "https": "http://%s" % p,
        }
        r = commons.get('https://m.douban.com', proxies=proxies)
        print(r.status_code)
        if r.status_code >= 300:
            proxy_list.remove(p)
    for p in proxy_list:
        print(p)

if __name__ == '__main__':
    main()

    