#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-18 20:14:05
from __future__ import print_function
import requests
import json
import shutil
import sys
import os
import traceback
import time
from requests import exceptions
from bs4 import BeautifulSoup
from urlparse import urlparse
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool

DEFAULT_TIMEOUT = 30
FILENAME_UNSAFE_CHARS = '/\\<>:?*"|'
USER_AGENT_DEAULT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.36 (KHTML, like Gecko) Chrome/43.0.1234.0 Safari/535.36'


def get_headers(url):
    headers = {}
    u = urlparse(url)
    headers['Referer'] = '{0}://{1}/'.format(u.scheme, u.netloc)
    headers['User-Agent'] = USER_AGENT_DEAULT
    return headers


def get_safe_filename(text):
    # text = text.replace(':', 'x')
    for c in FILENAME_UNSAFE_CHARS:
        if c in text:
            text = text.replace(c, "_")
    return text.strip()


def safe_rename(src, dst):
    try:
        shutil.move(src, dst)
    except OSError, e:
        print('{0} rename {1} to {1}'.format(e, src, dst))
    finally:
        if os.path.exists(src):
            os.remove(src)


def get(url, encoding=None, **options):
    r = requests.get(url, timeout=DEFAULT_TIMEOUT, headers=get_headers(url), **options)
    if encoding:
        r.encoding = encoding
    return r


def soup(url, encoding=None):
    r = get(url, encoding)
    return BeautifulSoup(r.text, 'html.parser')


def download_file(url, filename):
    tempfile = u'{0}.tmp'.format(filename)
    r = get(url)
    if r.status_code > 300:
        return url, None
    with open(tempfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8196):
            f.write(chunk)
    safe_rename(tempfile, filename)
    return url, filename


class Runner(object):

    def __init__(self, func, args, pool_size=4, retry=sys.maxint, sleep=60):
        self.func = func
        self.args = args
        self.pool_size = pool_size
        self.retry = retry
        self.sleep = sleep

    def start(self):
        while self.retry > 0:
            pool = ThreadPool(self.pool_size)
            try:
                pool.map(self.func, self.args)
                pool.close()
                pool.join()
                print('task execution completely.')
                break
            except KeyboardInterrupt, e:
                print('task terminated by user.', e)
                pool.terminate()
                pool.join()
                break
            except Exception, e:
                pool.terminate()
                pool.join()
                self.retry -= 1
                traceback.print_exc()
                print('task error: {0}, {1} retry in {2}s'.format(
                    e, sys.maxint - self.retry, 60))
                time.sleep(self.sleep)
