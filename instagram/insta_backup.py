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


def get_medias(user_id, all=False):
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    medias, next_ = api.user_recent_media(user_id=user_id, count=100)
    count = 10000 if all else 5
    while next_ and count > 0:
        print('next: %s' % next_)
        try:
            more_medias, next_ = api.user_recent_media(with_next_url=next_)
            if more_medias:
                medias.extend(more_medias)
            time.sleep(3)
        except Exception, e:
            print("error:%s on get_medias:%s" % (e, next_))
            time.sleep(10)
        count -= 1
    return medias


def process(user_id, all=False):
    download_files(get_medias(user_id, all))


def test(user_id):
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    medias, next_ = api.user_recent_media(user_id=user_id, count=10)
    for m in medias:
        print(m.created_time.strftime("%Y%m%d_%H%M%S"), m.get_standard_resolution_url())


if __name__ == '__main__':
    all = (len(sys.argv) > 2 and sys.argv[2] == '-a')
    process("1910999", all)
    print('finished at %s' % time.strftime("%Y-%m-%d %H:%M:%S"))
