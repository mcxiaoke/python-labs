#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-19 08:02:05

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from requests import exceptions
import re
import os
import sys
import codecs
import time
import Queue as queue
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
import json
import shutil
from urlparse import urlparse


INVALID_CHARS = '/\\<>:?*"|'


def get_safe_filename(text):
    text = text.replace(':', 'x')
    for c in INVALID_CHARS:
        if c in text:
            text = text.replace(c, "_")


'''
某个TAG的网址：http://www.umei.cc/tags/yongyi.htm

'''

vip_pattern = re.compile(u'xiuren_VIP')


def page_url(a):
    '''
     <DIV class=title><A href=http://www.umei.cc/p/gaoqing/xiuren_VIP/20150708150408.htm target=_blank title="【MiStar】 2015.07.08 VOL.021 Ashely丽丽 60P">【MiStar】 2015.07.08 VOL.021 Ashely丽丽 60P</A></DIV>
    '''
    return a.name == 'a' and a.get('href') and a.text and a.parent and a.parent.get('class') == ['title'] and not vip_pattern.search(a['href'])


def image_url(a):
    '''
    <img class=IMG_show border=0 src=http://i7.umei.cc//img2012/2015/08/07/012UTB201410223/02.jpg alt='[UTB] 2014.10 vol.222-223 宮脇咲良 小嶋真子 薮下柊 大島涼花 渡辺美優紀 岛崎遥香 向井地美音 森保西野木本[52P]'>
    '''
    return a.name == 'img' and a.get('class') == ['IMG_show']

# 查找某个TAG页面的所有专辑链接


def find_album_urls(tag_url):
    r = requests.get(tag_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    pages = soup.find_all(page_url)
    return [p.get('href') for p in pages]
    return filter(None, pages)


def find_image_urls(page_url):
    r = requests.get(page_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    print('process page', page_url)
    images = soup.find_all(image_url)
    return [img.get('src') for img in images]
    return filter(None, images)


def find_album_pages(album_url):
    r = requests.get(album_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title
    album = os.path.basename(album_url)[:-4]
    print('process album', album_url)
    links = soup.find_all(href=re.compile('{0}'.format(album)))
    page_url_pattern = album_url.replace(album, '{0}')[:-4]
    # print(page_url_pattern)
    pages = [page_url_pattern.format(l.get('href')) for l in links]
    return title, set(filter(None, pages))


def find_all_image_urls_for_album(album_url):
    urls=[]
    title, pages = find_album_pages(album_url)
    if not title or not pages:
        return
    for page in pages:
        images = find_image_urls(page)
        urls.extend(images)
        # for image in images:
        #     print(image)
    return sorted(urls)

start_url = 'http://www.umei.cc/tags/yongyi.htm'
albums = find_album_urls(start_url)
album = albums[10]
image_urls=find_all_image_urls_for_album(album)
for i in image_urls:
    print(i)
