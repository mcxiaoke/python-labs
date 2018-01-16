#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-25 08:45:45
from __future__ import print_function
from datetime import datetime
import codecs
import os
import sys
import requests
import shutil
import time
import json

def requests_to_curl(r):
    req = r.request
    method = req.method
    uri = req.url
    ct = req.headers.get('Content-Type')
    data = '[multipart]' if ct and 'multipart/form-data' in ct else (req.body or '')
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
        home =  pwd.getpwuid(os.getuid()).pw_dir
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
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
        return [line.rstrip('\n') for line in f]

def write_dict(name, dt):
    if not dt:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        json.dump(dt,f)

def read_dict(name):
    if not os.path.isfile(name):
        return {}
    with codecs.open(name, 'r', 'utf-8') as f:
        return json.load(f)
