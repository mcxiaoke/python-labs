#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-08 15:10:14
from __future__ import print_function, unicode_literals, absolute_import
import requests
import json
import os
import sys
import hashlib
import time
import argparse
import codecs
import re


def parse():
    ids = []
    with codecs.open('albums_data.py', 'r', 'utf-8') as f:
        lines = f.readlines()
        pat = re.compile(r'www\.douban\.com/doulist/(\d+)/')
        for line in lines:
            m = pat.search(line)
            if m:
                ids.append(m.group(1))
    print(ids)


def follow_all(ids):
    from doubanapi import ApiClient
    api = ApiClient()
    api.login(sys.argv[1], sys.argv[2])
    for i in ids:
        print('follow doulist {}'.format(i))
        api.doulist_follow(i)
        time.sleep(5)
