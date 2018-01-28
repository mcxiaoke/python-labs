#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-27 09:47:26
from __future__ import print_function, unicode_literals, absolute_import
import requests
import json
import os
import sys
import hashlib
import time
import argparse
import logging
from lxml import etree, html

sys.path.insert(1, os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
from lib import commons
from lib.utils import distinct_list, read_file

def parse_doulist():
    url = 'https://www.douban.com/doulist/39822487/?sort=time&sub_type=12'
    root = etree.HTML(commons.get(url).text)
    links = root.xpath('//a[contains(@href,"/photos/album/")]')
    return distinct_list([l.attrib['href'] for l in links])

def parse_douban_captcha():
    text = read_file(sys.argv[1])
    root = etree.HTML(text)
    captcha_image = root.xpath('//img[@id="captcha_image"]/@src')
    captcha_id = root.xpath('//input[@name="captcha-id"]/@value')
    if captcha_image and captcha_id:
        print(captcha_image[0])
        print(captcha_id[0])


if __name__ == '__main__':
    parse_douban_captcha()