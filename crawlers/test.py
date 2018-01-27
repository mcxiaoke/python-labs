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
from lxml import etree, html
from lxml.html.clean import Cleaner
import bs4
from bs4 import BeautifulSoup

def parse_list():
    url = 'https://www.douban.com/people/164799715/notes'
    r = commons.get(url)
    root = etree.HTML(r.text)
    items = root.xpath('//h3/a[contains(@href, "douban.com")]')
    next_url = root.xpath('//span[@class="next"]/a/@href')
    print(type(next_url))
    print(next_url)
    for item in items:
        title = item.text
        url = item.attrib['href']
        # title = item.xpath('text()')[0]
        # url = item.xpath('@href')[0]
        parsed_url = compat.urlparse(url)
        if 'note' not in parsed_url.path:
            url = compat.parse_qs(parsed_url.query)['url'][0]
        print('%s - %s' % (title, url))

def parse_one():
    url = 'https://www.douban.com/note/634157724/'
    r = commons.get(url)
    cleaner = Cleaner(page_structure=False, style=True, kill_tags=['ul', 'ol'])
    text = cleaner.clean_html(r.text)
    utils.write_file('a.html',text)
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.find(id='link-report')
    print(soup.title.text.strip())
    # print(body.prettify())
    imgs = soup('img')
    for img in imgs:
        iurl = img['src'].replace('/public/','/raw/')
        isrc = commons.download(iurl, 'output')
        img['src'] = isrc
        print(img)
    utils.write_file('b.html',soup.prettify())

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, commons, upath, utils
    parse_one()