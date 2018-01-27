#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-04 14:39:15
from __future__ import print_function, unicode_literals
import os
import sys
import codecs
import requests
import tweepy
from config import OWNER, OWNER_ID, CONSUMER_KEY, CONSUMER_SECRET, ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESSS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def read_list(name):
    if not os.path.isfile(name):
        return None
    with codecs.open(name, 'r', 'utf-8') as f:
        return [line.rstrip('\n') for line in f]


def add_to_list(slug, screen_name):
    print('add user: %s to list: %s' % (screen_name, slug))
    api.add_list_member(slug=slug,
                        screen_name=screen_name,
                        owner_screen_name='dorauimi')


def main():
    uids = read_list(sys.argv[1])
    for uid in uids:
        add_to_list('asiangirls', uid)

if __name__ == '__main__':
    main()
