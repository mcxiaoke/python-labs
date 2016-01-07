#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-21 08:32:34

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
from lib import commons

OUTPUT = 'output-aitaotu-images'
DOMAIN = 'http://www.aitaotu.com/'
INDEX_URL_TPL = 'http://www.aitaotu.com/guonei/list_{0}.html'

taotu_no_pattern = re.compile(u'/(\d+).html')
last_page_no_pattern = re.compile(u'_(\d+)\.html')


def filter_taotu_url(a):
    # 匹配某个页面的套图URL
    return a.name == 'a' and a.parent.name == 'span' and a.get('target')


def filter_last_page_tag(tag):
    # 匹配页面中末页两个字对应的链接
    return tag.name == 'a' and tag.text == u'末页'


def get_last_page_no(soup):
    # 找到某个页面分页序号末页对应的数字
    last = soup.find_all(filter_last_page_tag)[0]
    return int(last_page_no_pattern.search(last.get('href')).group(1))


def get_image_urls_for_taotu(url):
    # 找套图某一个页面包含的图片URL
    soup = commons.soup(url, encoding='utf8')
    imgs = soup.select('#big-pic')[0].find_all('img')
    urls = [img.get('src') for img in imgs]
    print('found {0} images in {1}'.format(len(urls), url))
    return urls


def download_taotu_images(turl, output=OUTPUT):
    # 下载某个套图的全部图片
    # http://www.aitaotu.com/guonei/5044.html
    # http://www.aitaotu.com/guonei/5044_10.html
    base_url = os.path.dirname(turl)
    page_no = os.path.basename(turl)[:-5]

    # 图片保存目录，用套图的No序号做目录名字
    img_dir = os.path.join(output, page_no)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # 如果发现 .dat 文件，表明这个套图已经全部下载完成，跳过
    stat_file = os.path.join(output, '{0}.dat'.format(page_no))
    if os.path.isfile(stat_file):
        print('skip done page: {0}'.format(turl))
        return

    print('downloading page: {0}'.format(turl))

    soup = commons.soup(turl, encoding='utf8')
    # print('process page: {0}'.format(soup.title))
    images = []
    # 找到这个套图所有页面的图片URL
    for i in range(2, get_last_page_no(soup) + 1):
        purl = '{0}/{1}_{2}.html'.format(base_url, page_no, i)
        images.extend(get_image_urls_for_taotu(purl))
    # 逐个下载图片
    for iurl in images:
        img_name = os.path.basename(iurl)
        img_file = os.path.join(img_dir, img_name)
        if os.path.isfile(img_file):
            # 如果图片已存在，跳过
            print('{0} skip image {1}'.format(page_no, img_file))
        else:
            # 不存在则下载
            print('{0} downloading {1}'.format(page_no, iurl))
            commons.download_file(iurl, img_file)
    # 没有发生异常全部下载完成，则保存状态文件
    with open(stat_file, 'wb') as f:
        pickle.dump(images, f)
    print('downloaded, save stat {0}'.format(turl))


def get_taotu_urls_for_page(url):
    # 找到某个页面包含的全部套图URL
    soup = commons.soup(url, encoding='utf8')
    links = soup.find_all(filter_taotu_url)
    return [urljoin(DOMAIN, l.get('href')) for l in links]


def download_by_page(url):
    # 遍历列表页面，逐页找到URL并下载
    print('process {0}'.format(url))
    taotu_urls = get_taotu_urls_for_page(url)
    for turl in taotu_urls:
        download_taotu_images(turl)


def get_taotu_pages(category_url):
    # 找到某个分类下全部的分页URL
    print('process category: {0}'.format(category_url))
    soup = commons.soup(category_url, encoding='utf8')
    print('process index: {0}'.format(soup.title))
    last_no = get_last_page_no(soup)
    urls = ['{0}/list_{1}.html'.format(category_url, i) for i in range(2, last_no + 1)]
    # for url in urls:
    # download_by_page(url)
    retry = 0
    while True:
        pool = ThreadPool(4)
        try:
            pool.map(download_by_page, urls)
            pool.close()
            pool.join()
            print('all images downloaded completely.')
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

if __name__ == '__main__':
    get_taotu_pages('http://www.aitaotu.com/guonei/')
    get_taotu_pages('http://www.aitaotu.com/rihan/')
    get_taotu_pages('http://www.aitaotu.com/gangtai/')
