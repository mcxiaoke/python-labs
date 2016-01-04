#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-12-30 10:14:13
from __future__ import print_function, unicode_literals
import sys
import os
import time
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


def download_files(urls, output='pics'):
    if not os.path.exists(output):
        os.makedirs(output)
    for url in urls:
        download_file(url, output)


def user_timeline(screen_name=None,
                  since_id=None,
                  max_id=None):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api.user_timeline(screen_name=screen_name,
                             since_id=since_id,
                             max_id=max_id,
                             count=200,
                             include_rts=True)


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
    for i in xrange(1, 20):
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
        write_list(url_path)
    urls = [u + ':large' for u in urls]
    download_files(urls, output=get_path('pics_%s' % user_id))


def get_path(path):
    return os.path.join('output', path)

if __name__ == '__main__':
    users = read_list('users.dat')
    for u in users:
        process(u)
    print('finished at %s' % time.strftime("%Y-%m-%d %H:%M:%S"))
