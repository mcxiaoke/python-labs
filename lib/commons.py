#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date: 2015-08-18 20:14:05
from __future__ import unicode_literals, division, absolute_import, print_function
import requests
import shutil
import sys
import signal
import os
import traceback
import time
import logging
import bs4
from lxml import html
from multiprocessing import Pool

from const import USER_AGENT_WIN, DEFAULT_REQUEST_TIMEOUT
from compat import urlparse, json
from utils import url_to_filename

logging.basicConfig(level=logging.DEBUG)

############################################################
#
# Network Functions
#
############################################################

default_timeout = DEFAULT_REQUEST_TIMEOUT


def get_headers(url):
    return {
        'Referer': '{0}://{1}/'.format(u.scheme, u.netloc),
        'User-Agent': '%s %s' % (USER_AGENT_WIN, time.time())
    }


def request(method, url, encoding=None, **kwargs):
    r = requests.request(method, url, timeout=default_timeout,
                         headers=get_headers(url), **kwargs)
    r.encoding = encoding or 'utf-8'
    if r.status_code >= 400:
        raise IOError("HTTP Status Code %s" % r.status_code)
    return r


def get(url, encoding=None, **kwargs):
    return request('get', url, encoding=encoding, **kwargs)


def post(url, encoding=None, **kwargs):
    return request('post', url, encoding=encoding, **kwargs)


def get_stream(url, encoding=None, **kwargs):
    return request('get', url, encoding=encoding, stream=True, **kwargs)


def clean_html(text, **kwargs):
    c = html.clean.Cleaner(page_structure=False, style=True, **kwargs)
    return c.clean_html(html.fromstring(text))


def soup(url, encoding=None, clean=False):
    r = get(url, encoding)
    text = clean_html(r.text) if clean else r.text
    return bs4.BeautifulSoup(text, 'html.parser')


def download_file(url, filename=None, output=None, **kwargs):
    filename = filename or url_to_filename(url)
    output = output or ''
    if not os.path.exists(output):
        os.mkdir(output)
    filepath = os.path.join(output, filename)
    if not os.path.exists(filepath):
        r = get_stream(url, **kwargs)
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            logging.info('Saved %s' % url)
    else:
        logging.info('Skip %s' % url)
    return filepath

############################################################
#
# Thread and Process Functions
#
############################################################
def run_in_thread(func, *args, **kwargs):
    """Run function in thread, return a Thread object"""
    from threading import Thread
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread


def run_in_subprocess(func, *args, **kwargs):
    """Run function in subprocess, return a Process object"""
    from multiprocessing import Process
    thread = Process(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

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
            logging.info('Task execution completely.')
            break
        except KeyboardInterrupt as e:
            logging.info('Task terminated by user.', e)
            pool.terminate()
            break
        except Exception as e:
            pool.terminate()
            retry += 1
            traceback.print_exc()
            if retry <= retry_max:
                next_delay = sleep * (retry % 6 + 1)
                logging.info('Task error: {0}, {1} retry in {2}s'.format(
                    e, retry_max - retry, next_delay))
                time.sleep(sleep * next_delay)
        finally:
            pool.join()
    return r.get()
