#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-25 08:45:45
from __future__ import print_function, unicode_literals
from datetime import datetime
import codecs
import os
import sys
import urllib
import requests
import shutil
import time
import json
import collections
import configparser
from . import compat

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

def import_src(name, fpath):
    import os
    import imp
    p = fpath if os.path.isabs(fpath) \
        else os.path.join(os.path.dirname(__file__), fpath)
    return imp.load_source(name, p)


def distinct_list(source_list, sort=False, reverse=False):
    result_list = collections.OrderedDict(
        (x, True) for x in source_list).keys()
    return sorted(result_list, reverse=reverse) if sort else result_list

def flatten_list(source_list):
    result_list = []
    for item in source_list:
        if isinstance(item, list):
            result_list.extend(item)
        else:
            result_list.append(item)
    return result_list

def url_filename(url):
    # return urlparse.urlparse(url).path
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]


def unquote_url(url):
    if isinstance(url, unicode):
        return urllib.unquote(url.encode('utf-8')).decode('utf-8')
    else:
        return urllib.unquote(url)


def requests_to_curl(r):
    req = r.request
    method = req.method
    uri = req.url
    ct = req.headers.get('Content-Type')
    data = '[multipart]' if ct and 'multipart/form-data' in ct else (
        req.body or '')
    headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    return command.format(method=method, headers=headers, data=data, uri=uri)


def get_user_home():
    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif os.name == 'posix':
        home = os.path.expanduser("~/")
    elif os.name == 'nt':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        import pwd
        home = pwd.getpwuid(os.getuid()).pw_dir
    return home


def get_current_user():
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user
    # If not user from os.environ.get()
    import pwd
    return pwd.getpwuid(os.getuid())[0]


def now():
    format_str = compat.unicode_str('%Y-%m-%d %H:%M:%S')
    return datetime.now().strftime(format_str)

def slice_list(l, n):
    """Yield successive n-sized chunks from l."""
    # for i in xrange(0, len(l), n):
    #     yield l[i:i + n]
    return [l[i:i + n] for i in range(0, len(l), n)]

def write_list(name, ls):
    if not ls:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return []
    with codecs.open(name, 'r', 'utf-8') as f:
        return filter(bool, [line.strip() for line in f])


def write_file(name, data):
    if not data:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        f.write(data)


def read_file(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return f.read()


def write_dict(name, dt):
    if not dt:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        json.dump(dt, f)


def read_dict(name):
    if not os.path.isfile(name):
        return {}
    with codecs.open(name, 'r', 'utf-8') as f:
        return json.load(f)


def aes_encrypt(data, secret='P2wH6eFqd8x4abnf'):
    # https://pypi.python.org/pypi/pycrypto
    from Crypto.Cipher import AES
    aes = AES.new(secret, AES.MODE_CBC, b'2017011720370117')
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    if len(data) % 16 != 0:
        data = data + str((16 - len(data) % 16) * '\0')
    return aes.encrypt(data)


def aes_decrypt(data, secret='P2wH6eFqd8x4abnf'):
    # https://pypi.python.org/pypi/pycrypto
    from Crypto.Cipher import AES
    aes = AES.new(secret, AES.MODE_CBC, b'2017011720370117')
    return aes.decrypt(data).rstrip('\0')


def main():
    text1 = u'哈哈哈哈啊哈哈和俄文32reewr'
    print(text1, type(text1))
    text2 = aes_decrypt(aes_encrypt(text1))
    print(text2, type(text2))


if __name__ == '__main__':
    main()
