#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-24 17:24:26
from __future__ import print_function
import requests
import json
import os
import hashlib
import time
from lib import commons

DFD_EDOMAIN='aHR0cHM6Ly9mcm9kby5kb3ViYW4uY29tL2FwaQ=='
DFD_EKEY='MGRhZDU1MWVjMGY4NGVkMDI5MDdmZjVjNDJlOGVjNzA='
DFD_ESECRET='OWU4YmI1NGRjMzI4OGNkZg=='
DFD_UA='YXBpLWNsaWVudC8xIGNvbS5kb3ViYW4uZnJvZG8vMi4xNC4yKDQyKSBBbmRyb2lkLzE5IGNhbmNyb193Y19sdGUgWGlhb21pIE1JIDRXICByb206bWl1aQ=='

# http://requests-docs-cn.readthedocs.org/zh_CN/latest/user/quickstart.html
API_KEY = '00a0951fbec80b0501e1bf5f3c58210f'
API_SECRET = '77faec137e9bda16'
# https://api.douban.com/v2/album/48382379/photos
ALBUM_PHOTOS_URL = 'http://api.douban.com/v2/album/{0}/photos'
# http://api.douban.com/v2/album/user_created/1376127
USER_ALBUMS_URL = 'http://api.douban.com/v2/album/user_created/{0}'
# http://www.douban.com/doulist/39822487/?sort=time&sub_type=12&start=0
DOULIST_PAGE_URL = 'http://www.douban.com/doulist/{0}/?sort=time&sub_type=12'
COUNT = 100
OUTPUT = 'output-douban-albums'

# start, count


def get_album_photos(album_id):
    url = ALBUM_PHOTOS_URL.format(album_id)
    print('正在处理相册 {0}'.format(url))
    urls = []
    album = None
    while True:
        queries = {}
        queries['apikey'] = API_KEY
        queries['udid'] = hashlib.sha1(url).hexdigest()
        queries['count'] = COUNT
        queries['start'] = len(urls)
        r = requests.get(url, params=queries)
        print('正在处理分页', r.url)
        if r.status_code < 300:
            data = json.loads(r.text)
            if not album:
                album = data['album']
            photos = data['photos']
            if not photos:
                break
            purls = [p.get('large') or p.get('image') for p in photos]
            urls.extend(purls)
            if len(photos) < COUNT:
                break
        time.sleep(2)
    print('相册[{0}]有{1}张图片'.format(album['title'].encode('utf8'), len(urls)))
    return album, urls


def download_album_photos(album, photos):
    if not album or not photos:
        return
    dirname = os.path.join(OUTPUT, album['id'])
    done_file = os.path.join(dirname, '.done')
    if os.path.exists(done_file):
        print('跳过已存在的相册[{0}]'.format(album['title'].encode('utf8')))
        return
    print('开始下载相册[{0}]的图片'.format(album['title'].encode('utf8')))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for photo in photos:
        name = photo.rsplit('/', 1)[1]
        imgfile = os.path.join(dirname, name)
        if not os.path.exists(imgfile):
            u, n = commons.download_file(photo, imgfile)
            if n:
                print('完成下载 {0}'.format(photo))
    with open(done_file, 'w') as f:
        f.write(utis.now())
    print('相册[{0}]的图片下载完成'.format(album['title'].encode('utf8')))


def download_by_album(id):
    album, photos = get_album_photos(id)
    download_album_photos(album, photos)


def download_by_people(userid):
    pass


def doulist_album_url_pattern(tag):
    return (tag.name == 'a' and tag.parent.get('class') == ['title'])


def get_albums_in_doulist_page(url):
    soup = commons.soup(url)
    links = soup.find_all(doulist_album_url_pattern)
    return filter(None, [a.get('href') for a in links])


def get_albums_in_doulist(id):
    url = DOULIST_PAGE_URL.format(id)
    print('正在处理豆列 {0}'.format(url))
    urls = []
    start = 0
    while True:
        page_url = '{0}&start={1}'.format(url, start)
        print('processing {0}'.format(page_url))
        purls = get_albums_in_doulist_page(page_url)
        if not purls:
            break
        print('found {0} albums'.format(len(purls)))
        urls.extend(purls)
        # 豆列每页25项
        if len(purls) < 20:
            break
        start += 25
        time.sleep(5)
    print('豆列[{0}]包含{1}个相册'.format(url, len(urls)))
    return urls


def download_by_doulist(id):
    albums = get_albums_in_doulist(id)
    for album in albums:
        download_by_album(album)


if __name__ == '__main__':
    # download_by_album('48382379')
    get_albums_in_doulist('39822487')
