#!/usr/bin/env python3
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

def main():
    url = 'https://www.douban.com/people/theanna/notes'
    r = commons.get(url)
    root = etree.HTML(r.text)
    items = root.xpath('//h3/a[contains(@href, "douban.com")]')
    for item in items:
        title = item.text
        url = item.attrib['href']
        # title = item.xpath('text()')[0]
        # url = item.xpath('@href')[0]
        parsed_url = compat.urlparse(url)
        if 'note' not in parsed_url.path:
            url = compat.parse_qs(parsed_url.query)['url'][0]
        print('%s - %s' % (title, url))

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, commons, upath, utils
    main()