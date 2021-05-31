#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-19 08:02:05

from __future__ import print_function
from requests import exceptions
import re
import os
import sys
import codecs
import time
import pickle
import Queue as queue
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
import json
import shutil
import traceback
from urlparse import urlparse
from urlparse import urljoin
from lib import commons, utils

DOMAIN = 'http://www.umei.cc/'
# 标签页URL
TAG_URL_TPL = 'http://www.umei.cc/tags/{0}.htm'
# 列表页URL
INDEX_URL_TPL = 'http://www.umei.cc/p/gaoqing/index-{0}.htm'

OUTPUT_DIR = 'output-umeicc-images'

# 过滤掉VIP标签
vip_pattern = re.compile(u'xiuren_VIP')
# 提取标签
tag_pattern = re.compile(u'http://www.umei.cc/tags/(\S+)\.htm')

# 匹配某个专辑的URL


def page_url_pattern(tag):
    '''
     <DIV class=title><A href=http://www.umei.cc/p/gaoqing/xiuren_VIP/20150708150408.htm
     target=_blank title="【MiStar】 2015.07.08 VOL.021 Ashely丽丽 60P">
     【MiStar】 2015.07.08 VOL.021 Ashely丽丽 60P</A></DIV>
    '''
    return (tag.name == 'a' and tag.get('href') and
            tag.text and tag.parent and
            tag.parent.get('class') == ['title'] and not
            vip_pattern.search(tag['href']))

# 匹配专辑页面的图片URL


def image_url_pattern(tag):
    '''
    <img class=IMG_show border=0 src=http://i7.umei.cc//img2012/2015/08/07/012UTB201410223/02.jpg
    alt='[UTB] 2014.10 vol.222-223 宮脇咲良 小嶋真子 薮下柊 大島涼花
     渡辺美優紀 岛崎遥香 向井地美音 森保西野木本[52P]'>
    '''
    return (tag.name == 'img' and tag.get('class') == ['IMG_show'])


def find_album_urls_by_tag(url):
    # 查找某个TAG页面的所有专辑URL
    # print('finding albums in {0}'.format(url))
    soup = commons.soup(url, encoding='gbk')
    pages = soup.find_all(page_url_pattern)
    return [p.get('href') for p in pages]
    return filter(None, pages)


def find_album_urls_by_index(url):
    # 查找某个列表页面的所有专辑URL
    # print('finding albums in {0}'.format(url))
    soup = commons.soup(url, encoding='gbk')
    pages = soup.find_all(page_url_pattern)
    return [urljoin(DOMAIN, p.get('href')) for p in pages]


def find_image_urls(page_url):
    # 查找某个图片页面的所有图片URL
    soup = commons.soup(page_url, encoding='gbk')
    # print('process page', page_url)
    images = soup.find_all(image_url_pattern)
    return [img.get('src') for img in images]
    return filter(None, images)


def find_album_pages(album_url):
    # 查找某个专辑页面的所有分页URL
    soup = commons.soup(album_url, encoding='gbk')
    title = soup.title
    album = os.path.basename(album_url)[:-4]
    print('process album', album_url)
    links = soup.find_all(href=re.compile('{0}'.format(album)))
    page_url_pattern = album_url.replace(album, '{0}')[:-4]
    # print(page_url_pattern)
    pages = [page_url_pattern.format(l.get('href')) for l in links]
    return title.text, set(filter(None, pages))


def find_all_image_urls_for_album(album_url):
    # 查找某个专辑包含的所有图片URL
    urls = []
    title, pages = find_album_pages(album_url)
    if not title or not pages:
        return
    for page in pages:
        print('process {0}'.format(page, album_url))
        images = find_image_urls(page)
        urls.extend(images)
        # for image in images:
        #     print(image)
    return title, sorted(urls)


def download_image(url, img_dir):
    # 下载某一张图片
    img_name = url.rsplit('/', 1)[1]
    img_file = os.path.join(img_dir, img_name)
    if os.path.isfile(img_file):
        # print(u'skip exists image: {0}'.format(url))
        return
    print(u'downloading {0}'.format(url))
    u, n = commons.download_file(url, img_file)
    if u and n:
        print(u'saved {0}'.format(img_file))
    else:
        print(u'not found {0}'.format(url))


def download_by_album(album_url, output=OUTPUT_DIR):
    # 下载某个专辑的全部图片
    stat_dir = os.path.join(output, 'stats')
    if not os.path.exists(stat_dir):
        os.makedirs(stat_dir)
    album_key = utils.url_to_filename(album_url)
    # 下载完成文件
    album_done_file = os.path.join(
        stat_dir, 'album_{0}.done'.format(album_key))
    if os.path.isfile(album_done_file):
        # 已存在，则跳过
        print('skip album: {0}'.format(album_url))
        return

# 读取数据文件
    album_stat_file = os.path.join(stat_dir, 'album_{0}.dat'.format(album_key))

    title, urls = None, None
    if os.path.isfile(album_stat_file):
        with open(album_stat_file, 'rb') as f:
            title, urls = pickle.load(f)
    if not title or not urls:
        # 不存在数据缓存，从网络获取
        print(u'no cache for {0}'.format(album_url))
        title, urls = find_all_image_urls_for_album(album_url)
    else:
        print(u'found cache for {0}'.format(album_url))
    if not title or not urls:
        print(u'no data, skip {0}'.format(album_url))
        return
    with open(album_stat_file, 'wb') as f:
        pickle.dump((title, urls), f)
    print(u'downloading album {0} - {1}'.format(title, album_url))
    print(u'found {0} images in {1}'.format(len(urls), title))
    album_name = utils.get_valid_filename(title)
    img_dir = os.path.join(output, album_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # 逐个下载图片
    for url in urls:
        download_image(url, img_dir)
    # 写入完成状态文件
    with open(album_done_file, 'w') as f:
        f.write(album_url)


def download_by_tag(tag, output=OUTPUT_DIR):
    # 下载某个标签下的全部专辑的图片
    print('processing tag: {0}'.format(tag))
    url = TAG_URL_TPL.format(tag)
    albums = find_album_urls_by_tag(url)
    for album in albums:
        download_by_album(album, output)


def download_by_page(page, output=OUTPUT_DIR):
    print('processing page: {0}'.format(page))
    url = INDEX_URL_TPL.format(page)
    albums = find_album_urls_by_index(url)
    for album in albums:
        download_by_album(album, output)


def dowload_all(by_page=False):
    # 下载全站标签对应的图片
    items = range(1, 145) if by_page else get_all_tags()
    retry = 0
    while True:
        pool = ThreadPool(4)
        try:
            pool.map(download_by_page if by_page else download_by_tag, items)
            pool.close()
            pool.join()
            print('all images are downloaded completely.')
            break
        except KeyboardInterrupt, e:
            print('download terminated by user, quit now.', e)
            pool.terminate()
            pool.join()
            break
        except Exception, e:
            pool.terminate()
            pool.join()
            retry += 1
            traceback.print_exc()
            try:
                print('download error: {0}, {1} retry in {2}s'.format(
                    e, retry, retry * 20 % 120))
            except Exception:
                pass
            time.sleep(retry * 20 % 120)


def get_all_tags():
    # 获取所有标签，去重
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    tags_file = os.path.join(OUTPUT_DIR, 'tags.dat')
    if os.path.isfile(tags_file):
        with open(tags_file, 'rb') as f:
            print('found tags cache, skip fetch remote tags')
            return pickle.load(f)
    # get tags from tags page
    url = 'http://www.umei.cc/tags/'
    soup = commons.soup(url, encoding='gbk')
    urls = soup.find_all(href=tag_pattern)
    tags = [tag_pattern.match(a.get('href')).group(1) for a in urls]
    # get tags from index page
    url = 'http://www.umei.cc/'
    soup = commons.soup(url, encoding='gbk')
    urls = soup.find_all(href=tag_pattern)
    tags.extend([tag_pattern.match(a.get('href')).group(1) for a in urls])
    with open(tags_file, 'wb') as f:
        pickle.dump(tags, f)
    return sorted(set(tags))

if __name__ == '__main__':
    print(sorted(get_all_tags()))
    by_page = len(sys.argv) == 2 and sys.argv[1] == '-p'
    print('starting download umei.cc images by {0}'.format('page' if by_page else 'tag'))
    dowload_all(by_page)
