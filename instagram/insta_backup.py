#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 11:14:57
from __future__ import print_function, unicode_literals
import time
import sys
import os
import pprint
from instagram.client import InstagramAPI
from utils import to_dict, write_list, read_list, download_insta_files
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, ACCESS_TOKEN


def get_media_urls(medias):
    urls = []
    if medias:
        for media in medias:
            url = media.get_standard_resolution_url() or media.get_low_resolution_url()
            urls.append(url.replace('s640x640/sh0.08/', ''))
    return urls


def get_medias(user_id, all=False):
    print('get_medias user_id=%s, all=%s' % (user_id, all))
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    medias = []
    # media_urls = []
    more_medias, _ = api.user_recent_media()
    # media_urls.extend(get_media_urls(more_medias))
    if more_medias:
        medias.extend(more_medias)
    loop = 100 if all else 1
    while more_medias and loop > 0:
        try:
            print('get_medias max_id=%s' % more_medias[-1].id)
            more_medias, _ = api.user_recent_media(max_id=more_medias[-1].id)
            if not more_medias:
                print('get_medias no more data, break')
                break
            print('get_medias new medias count: %s' % len(more_medias))
            medias.extend(more_medias)
            # media_urls.extend(get_media_urls(more_medias))
            time.sleep(3)
        except Exception, e:
            print("error:%s on get_medias:%s" % (e, loop))
            time.sleep(10)
        loop -= 1
    return medias


def process(user_id, all=False):
    print('process user_id=%s, all=%s' % (user_id, all))
    medias = get_medias(user_id, all)
    for m in medias:
        d = to_dict(m)
        pprint.pprint(d)
    if all:
        print('medias total: %s' % len(medias))
        urls = [m.get_standard_resolution_url() for m in medias]
        write_list(u'%s_list.txt' % user_id, urls)
        download_insta_files(get_medias(user_id, all), output=user_id)


def test(user_id):
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    medias, next_ = api.user_recent_media(user_id=user_id, count=10)
    for m in medias:
        print(m.created_time.strftime("%Y%m%d_%H%M%S"), m.get_standard_resolution_url())


if __name__ == '__main__':
    all = (len(sys.argv) >= 2 and sys.argv[1] == '-a')
    print(sys.argv)
    process("1910999", all)
    #print('finished at %s' % time.strftime("%Y-%m-%d %H:%M:%S"))
