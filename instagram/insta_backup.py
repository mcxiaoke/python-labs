#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 11:14:57
from __future__ import print_function, unicode_literals
import time
import sys
import os
from instagram.client import InstagramAPI
from utils import write_list, read_list, download_files
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ACCESS_TOKEN


def get_urls(user_id):
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    medias, next_ = api.user_recent_media(user_id=user_id, count=100)
    while next_:
        print('next: %s' % next_)
        more_medias, next_ = api.user_recent_media(with_next_url=next_)
        if more_medias:
            medias.extend(more_medias)
    urls = [media.get_standard_resolution_url() for media in medias]
    write_list('urls_%s.txt' % user_id, urls)
    for u in urls:
        print(u)


def process(user_id):
    print('download pics for user %s' % user_id)
    urls = read_list('urls_%s.txt' % user_id)
    if not urls:
        urls = get_urls(user_id)
        write_list('urls_%s.txt' % user_id, urls)
    download_files(urls)


if __name__ == '__main__':
    process("1910999")
    print('finished at %s' % time.strftime("%Y-%m-%d %H:%M:%S"))
