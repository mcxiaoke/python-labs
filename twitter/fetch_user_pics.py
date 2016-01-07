#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-12-30 10:14:13
from __future__ import print_function, unicode_literals
import sys
import os
import time
import shutil
import codecs
import requests
import tweepy
from config import OWNER, OWNER_ID, CONSUMER_KEY, CONSUMER_SECRET, ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET

'''
https://github.com/bear/python-twitter/
http://tweepy.readthedocs.org/en/v3.5.0/api.html

https://dev.twitter.com/rest/public/rate-limits
https://dev.twitter.com/rest/reference/get/statuses/user_timeline
https://dev.twitter.com/overview/api/entities-in-twitter-objects#media
'''

MIN_SIZE = 30 * 1024 * 1024  # skip size < 30k

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.1234.0 Safari/537.36',
           'Referer': 'https://twitter.com/'}


def write_list(name, ls):
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return [line.rstrip('\n') for line in f]


def download_file(url, output='pics'):
    # print('url:%s, output:%s' % (url, output))
    name = url.split('/')[-1].replace(':large', '')
    path = os.path.abspath(os.path.join(output, name))
    skippath = os.path.abspath(os.path.join(output, name + ".0"))
    tmppath = os.path.abspath(os.path.join(output, name + ".tmp"))
    # check file exists , check skip file exists
    if os.path.isfile(path) or os.path.isfile(skippath):
        # print('skip exists %s' % url)
        return None
    try:
        r = requests.get(url, stream=True, headers=HEADERS)
        length = int(r.headers['Content-Length'])
        # skip url when length < MIN_SIZE
        if length < MIN_SIZE:
            print('skip small %s' % url)
            with open(skippath, 'w') as f:
                f.write('0')
            return None
        print('downloading %s (%sk)' % (url, length / 2014))
        if r.status_code == requests.codes.ok:
            with open(tmppath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=4096):
                    f.write(chunk)
            shutil.move(tmppath, path)
            print('downloaded: %s' % path)
            return path
    except Exception as e:
        print("error:%s on %s" % (e, url))


def download_files(urls, output='pics'):
    if not os.path.exists(output):
        os.makedirs(output)
    for url in urls:
        download_file(url, output)


def download_files2(urls, output='pics'):
    if not os.path.exists(output):
        os.makedirs(output)
    from multiprocessing.dummy import Pool
    from functools import partial
    partial_download_file = partial(download_file, output=output)
    pool = Pool(4)
    pool.map(partial_download_file, urls)
    pool.close()
    pool.join()


def user_timeline(screen_name=None,
                  since_id=None,
                  max_id=None):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        return api.user_timeline(screen_name=screen_name,
                                 since_id=since_id,
                                 max_id=max_id,
                                 count=200,
                                 include_rts=True)
    except Exception, e:
        print("error:%s on user_timeline for %s" % (e, screen_name))


def extract_url(s):
    if s and s.entities and s.entities.get('media'):
        url = s.entities['media'][0]['media_url']
        if url and url.endswith('.jpg'):
            return url


def extract_urls(ss):
    if not ss:
        return []
    return filter(None, [extract_url(s) for s in ss])


def get_picture_urls(user_id, loop=10):
    urls = []
    ss = None
    max_id = None
    for i in xrange(1, loop):
        print('page:%s, max_id:%s, total:%s' % (i, max_id, len(urls)))
        ss = user_timeline(screen_name=user_id, max_id=max_id)
        if not ss:
            break
        if ss[-1].id == max_id:
            break
        max_id = ss[-1].id
        urls.extend(extract_urls(ss))
    return filter(None, urls)


def process(user_id):
    print('download pics for user %s' % user_id)
    url_path = get_path('urls_%s.txt' % user_id)
    urls = read_list(url_path)
    if not urls:
        urls = get_picture_urls(user_id)
        write_list(url_path, urls)
    urls = [u + ':large' for u in urls]
    download_files2(urls, output=get_path('pics_%s' % user_id))


def get_path(path):
    return os.path.join('output', path)

if __name__ == '__main__':
    users = read_list('users.dat')
    for u in users:
        process(u)
    print('finished at %s' % time.strftime("%Y-%m-%d %H:%M:%S"))
