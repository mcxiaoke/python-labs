#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 11:18:06
import codecs
import os
import sys
import requests
import shutil
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.1234.0 Safari/537.36',
           'Referer': 'https://google.com/'}


def write_list(name, ls):
    if not ls:
        return
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return [line.rstrip('\n') for line in f]


def download_file(media, output='output'):
    # print('url:%s, output:%s' % (url, output))
    url = media.get_standard_resolution_url().replace('/s640x640/', '/')
    name = url.split('/')[-1].split("?ig_cache_key=")[0]
    fname = media.created_time.strftime("%Y%m%d_%H%M%S") + "_" + name
    print(fname)
    tmpname = name + ".tmp"
    fpath = os.path.abspath(os.path.join(output, fname))
    path = os.path.abspath(os.path.join(output, name))
    tmppath = os.path.abspath(os.path.join(output, tmpname))
    if os.path.isfile(fpath):
        print('skip exists %s' % path)
        return fpath
    if os.path.isfile(path):
        print('skip exists %s' % path)
        shutil.move(path,fpath)
        return fpath
    try:
        r = requests.get(url, stream=True, headers=HEADERS)
        length = int(r.headers['Content-Length'])
        print('downloading %s (%sk)' % (url, length / 2014))
        if r.status_code == requests.codes.ok:
            with open(tmppath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
            shutil.move(tmppath, fpath)
            #print('saved to %s' % path)
            return fpath
    except Exception as e:
        print("error:%s on downloading file:%s" % (e, url))


def download_files(medias, output='output'):
    if not os.path.exists(output):
        os.makedirs(output)
    for media in medias:
        download_file(media, output)


def download_files_multi(urls, output='files', pool_size=4):
    if not os.path.exists(output):
        os.makedirs(output)
    from multiprocessing.dummy import Pool
    from functools import partial
    partial_download_file = partial(download_file, output=output)
    pool = Pool(pool_size)
    pool.map(partial_download_file, urls)
    pool.close()
    pool.join()
