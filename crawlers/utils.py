#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-25 08:45:45

from datetime import datetime
import codecs
import os
import sys
import requests
import shutil
import time
import json

def check_login(func):
    def __decorator():
        print('enter the login')
        func()
        print('exit the login')
    return __decorator

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
