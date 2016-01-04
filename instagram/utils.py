#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 11:18:06
import codecs
import os
import sys
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.1234.0 Safari/537.36',
           'Referer': 'https://google.com/'}


def write_list(name, ls):
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return [line.rstrip('\n') for line in f]


def download_file(url, output='files'):
    name = url.split('/')[-1]
    path = os.path.abspath(os.path.join(output, name))
    if os.path.isfile(path):
        print('skip exists %s' % path)
        return path
    try:
        r = requests.get(url, stream=True, headers=HEADERS)
        length = int(r.headers['Content-Length'])
        print('downloading %s size: %sk' % (url, length / 2014))
        if r.status_code == requests.codes.ok:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
            print('saved to %s' % path)
            return path
    except Exception as e:
        print("error:%s on downloading file:%s" % (e, url))


def download_files(urls, output='files'):
    if not os.path.exists(output):
        os.makedirs(output)
    for url in urls:
        download_file(url, output)
