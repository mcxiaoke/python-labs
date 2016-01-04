#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 15:37:58
from __future__ import print_function, unicode_literals
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET
import os
import sys
import shutil
import codecs
import pytumblr


def write_list(name, ls):
    with codecs.open(name, 'w', 'utf-8') as f:
        for s in ls:
            f.write(s + '\n')


def read_list(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return [line.rstrip('\n') for line in f]

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESSS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET
)


def get_urls(blog):
    offset = 0
    response = client.posts(blog, type='photo', offset=offset)
    posts = response['posts']
    while offset < 400:
        r = client.posts(blog, type='photo', offset=offset)
        p = r['posts']
        if not p:
            break
        posts.extend(p)
        offset = offset + 20

    urls = [p['photos'][0]['original_size']['url'] for p in posts]
    for u in urls:
        print(u)
    return urls


def main():
    write_list('urls.txt', get_urls('tr20150104.tumblr.com'))

if __name__ == '__main__':
    main()
