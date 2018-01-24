#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-18 20:14:05
from __future__ import print_function
import requests
import json
import shutil
import sys
import signal
import os
import traceback
import time
from requests import exceptions
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
from .compat import urlparse

class HTTPError(Exception):
    def __init__(self, message, code):
        # Call the base class constructor with the parameters it needs
        super(HTTPError, self).__init__(message)
        # Now for your custom code...
        self.code = code


DEFAULT_TIMEOUT = 30
FILENAME_UNSAFE_CHARS = '/\\<>:?*"|'
USER_AGENT_OSX = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
USER_AGENT_WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
USER_AGENT_MOBILE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1'

is_mobile = False


def get_user_agent():
    return USER_AGENT_MOBILE if is_mobile else USER_AGENT_WIN


def get_headers(url):
    headers = {}
    u = urlparse(url)
    headers['Referer'] = '{0}://{1}/'.format(u.scheme, u.netloc)
    headers['User-Agent'] = get_user_agent()
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
    except OSError as e:
        print('{0} rename {1} to {1}'.format(e, src, dst))
    finally:
        if os.path.exists(src):
            os.remove(src)


def get(url, encoding=None, **options):
    r = requests.get(url, timeout=DEFAULT_TIMEOUT,
                     headers=get_headers(url), **options)
    if encoding:
        r.encoding = encoding
    else:
        r.encoding = 'utf-8'
    if r.status_code >= 400:
        raise IOError("HTTP Status Code %s" % r.status_code)
    return r


def soup(url, encoding=None):
    r = get(url, encoding)
    soup = BeautifulSoup(r.text, 'html.parser')
    for s in soup('script'):
        s.decompose()
    for s in soup('style'):
        s.decompose()
    return soup


def download_file(url, filename):
    tempfile = u'{0}.tmp'.format(filename)
    r = get(url)
    if r.status_code >= 300:
        raise IOError("HTTP Status Code %s" % r.status_code)
    with open(tempfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=40960):
            f.write(chunk)
    safe_rename(tempfile, filename)
    return url, filename


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def run_in_pool(func, args, pool_size=4, retry_max=0, sleep=60):
    def _initializer():
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    r = None
    retry = 0
    while retry <= retry_max:
        pool = Pool(pool_size, _initializer)
        try:
            r = pool.map_async(func, args)
            r.get(999999)
            pool.close()
            print('Task execution completely.')
            break
        except KeyboardInterrupt as e:
            print('Task terminated by user.', e)
            pool.terminate()
            break
        except Exception as e:
            pool.terminate()
            retry += 1
            traceback.print_exc()
            if retry <= retry_max:
                next_delay = sleep * (retry%6+1)
                print('Task error: {0}, {1} retry in {2}s'.format(
                    e, retry_max - retry, next_delay))
                time.sleep(sleep * next_delay)
        finally:
            pool.join()
    return r.get()
