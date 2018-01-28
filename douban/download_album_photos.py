#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-24 17:24:26
from __future__ import print_function, unicode_literals, absolute_import
import requests
import json
import os
import sys
import hashlib
import time
import argparse
import logging
from lxml import etree, html

logging.basicConfig(level=logging.INFO)

__version__ = '1.0.0'

DFD_EDOMAIN = 'aHR0cHM6Ly9mcm9kby5kb3ViYW4uY29tL2FwaQ=='
DFD_EKEY = 'MGRhZDU1MWVjMGY4NGVkMDI5MDdmZjVjNDJlOGVjNzA='
DFD_ESECRET = 'OWU4YmI1NGRjMzI4OGNkZg=='
DFD_UA = 'YXBpLWNsaWVudC8xIGNvbS5kb3ViYW4uZnJvZG8vMi4xNC4yKDQyKSBBbmRyb2lkLzE5IGNhbmNyb193Y19sdGUgWGlhb21pIE1JIDRXICByb206bWl1aQ=='

# http://requests-docs-cn.readthedocs.org/zh_CN/latest/user/quickstart.html
API_KEY = '00a0951fbec80b0501e1bf5f3c58210f'
API_SECRET = '77faec137e9bda16'
# https://api.douban.com/v2/album/48382379/photos
ALBUM_PHOTOS_URL = 'http://api.douban.com/v2/album/{0}/photos'
# http://api.douban.com/v2/album/user_created/1376127
USER_ALBUMS_URL = 'http://api.douban.com/v2/album/user_created/{0}'
# http://www.douban.com/doulist/39822487/?sort=time&sub_type=12&start=0
DOULIST_PAGE_URL = 'http://www.douban.com/doulist/%s/?sort=time&sub_type=12&start=%s'
COUNT = 100
COUNT_IN_DOULIST_PAGE = 25

def download_by_doulist(id):
    albums = get_albums_in_doulist(id)
    for album in albums:
        download_by_album(album)


def download_by_user(userid):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Douban Albums Downloader v{0}'.format(__version__),
        epilog='''https://github.com/mcxiaoke/python-labs
        ''')
    parser.add_argument('-a', '--album',
                        help='Album Id')
    parser.add_argument('-l', '--doulist',
                        help='Doulist Id')
    parser.add_argument('-u', '--userid',
                        help='User Id')
    parser.add_argument('-o', '--output',
                        help='Save Destination')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import commons
    if True:
        # from doubanutils import get_album_photos,download_album_photos, get_doulist_album_urls
        # album, photos = get_album_photos('1625987334')
        # download_album_photos('1633284105')
        # download_album_photos(1622166069)
        # get_doulist_album_urls('39822487')
        exit(0)
    args = vars(parse_args())
    print(args)
    if args.get('album'):
        download_by_album(args['album'])
    elif args.get('doulist'):
        download_by_doulist(args['doulist'])
    elif args.get('userid'):
        download_by_user(args['userid'])
