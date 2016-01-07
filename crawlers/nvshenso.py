#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-24 10:49:24

from __future__ import print_function
from requests import exceptions
import re
import os
import sys
import codecs
import time
import pickle
import Queue as queue
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
from urlparse import urlparse
from urlparse import urljoin
from lib import commons

OUTPUT = 'output-nvshenso-images'
URL_TPL = 'http://www.nvshen.so/wp-content/uploads/2015/{0}/{1}.jpg'


def download_by_month(month):
    print('processing month ', month)
    dest = os.path.join(OUTPUT, unicode(month))
    if not os.path.exists(dest):
        os.makedirs(dest)
    for i in range(1300):
        url = URL_TPL.format(month, i)
        name = url.rsplit('/', 1)[1]
        filename = os.path.join(dest, name)
        nofile = '{0}.bad'.format(filename)
        if os.path.exists(filename) or os.path.exists(nofile):
            print('skip ', url)
            continue
        # print('downloading ', url)
        u, n = commons.download_file(url, filename)
        if n:
            print('image saved ', url)
        else:
            with open(nofile, 'w') as f:
                f.write(url)


def download_year_2015():
    months = ['%02d' % i for i in range(1, 9)]
    runner = commons.Runner(download_by_month, months)
    runner.start()
    # for i in range(8, 0, -1):
    #     download_by_month(i)


if __name__ == '__main__':
    download_year_2015()
