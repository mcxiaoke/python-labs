#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import sys
import os
import re
import time
import shutil
import random
import requests
import sqlite3
from builtins import *

TABLE_NAME = 'poetry_of_tang'
TABLE_NAME_FTS = 'poetry_of_tang_fts4'

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print ('%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0))
        return ret
    return wrap

@timing
def read_text():
    results = []
    with codecs.open('poetry.txt', 'r', 'utf-8') as f:
        lines = f.read().splitlines()
        values = [tuple(l.split(':')) for l in lines]
        for line in lines:
            if '猫' in line:
                results.append(line)
    return results
                

# c = sqlite3.connect('poetry.db')
# for v in values:
    # c.execute('INSERT INTO poetry_of_tang VALUES (?,?)', v)
# c.executemany('INSERT INTO poetry_of_tang VALUES (?,?)', values)
# c.commit()

def main():
    print(time.strftime('%Y-%m-%d %H:%M:%S.%s'))
    read_text()
    print(time.strftime('%Y-%m-%d %H:%M:%S.%s'))

if __name__ == '__main__':
    main()
