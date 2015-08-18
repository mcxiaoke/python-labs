#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 08:35:05
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
from utils import get_safe_filename

OUTPUT = 'output'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.1234.0 Safari/537.36',
           'Referer': 'http://www.dapenti.com/'}

# page
url_tpl = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei&page={0}'
page_tpl = 'http://www.dapenti.com/blog/more.asp?name=xilei&id={0}'  # id

urls = []
lock = Lock()

url_date_pat = re.compile(u'【\S+(\d{8})】')
url_id_pat = re.compile(u'&id=(\d+)')


def url_cmp(ua, ub):
    a = url_date_pat.search(ua.text).group(1)
    b = url_date_pat.search(ub.text).group(1)
    # print(a.encode('utf8'),b.encode('utf8'))
    return cmp(b, a)


def myurl(a):
    return a.get('href') and a.text and a.parent.name == 'li' and re.compile(u'\S+图卦\d{8}】.+').search(a.text)


def findurls(page):
    print('fetch page ' + str(page))
    url = url_tpl.format(page)
    r = requests.get(url, timeout=20, headers=HEADERS)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(myurl)
    if links:
        print('fetch page ' + str(page) + 'found links ' + str(len(links)))
        lock.acquire()
        urls.extend(links)
        lock.release()
    return links


def safe_rename(src, dst):
    try:
        shutil.move(src, dst)
    except OSError, e:
        print('{0} rename {1} to {1}'.format(e, src, dst))
    finally:
        if os.path.exists(src):
            os.remove(src)

def fix_img_url(src):
    return src.replace('imgs.dapenti.org:88','ptimg.org:88')

def download_image(url, filename, id):
    url=fix_img_url(url)
    print('download image for {0}: {1}'.format(id, url))
    tempfile = '{0}.tmp'.format(filename)
    r = requests.get(url, timeout=20, headers=HEADERS)
    if r.status_code == 404:
        return url, None
    with open(tempfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    safe_rename(tempfile, filename)
    return url, filename
    # print('image saved {0}'.format(url))


def download_page(item):
    id = item['id']
    url = page_tpl.format(id)
    filename = os.path.join(OUTPUT, '{}.html'.format(id))
    if os.path.exists(filename):
        print('skip page {0}'.format(url))
        return
    print('download page: {0}'.format(url))
    r = requests.get(url, timeout=20, headers=HEADERS)
    # 必须用gbk，要不然繁体乱码
    # 虽然网页上写的是gb2312，但是浏览器实际使用的是gbk
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, 'html.parser')
    imgs = soup.find_all('img')
    img_dirname = 'images_{0}'.format(id)
    imgdir = os.path.join(OUTPUT, img_dirname)
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)

    for img in imgs:
        from_src = img['src']
        if not from_src.startswith('http://'):
            from_src = 'http://www.dapenti.com/blog/{0}'.format(from_src)
        to_src = get_safe_filename(from_src)
        imgfile = os.path.join(imgdir, to_src)
        img['src'] = os.path.join(img_dirname, to_src)
        if os.path.exists(imgfile):
            print('skip exists image {0}'.format(from_src))
        else:
            iurl,iname=download_image(from_src, imgfile, id)
            if  not iname:
                # 如果图片无法下载，保留原始URL
                img['src']=from_src
    tempfile = '{0}.tmp'.format(filename)
    with open(tempfile, 'w') as f:
        # 用utf写入文件，所以html头的gb2312需要改为utf8
        content = unicode(soup).replace('charset=gb2312', 'charset=utf-8')
        f.write(content.encode('utf8'))
    safe_rename(tempfile, filename)
    print('page saved {0}'.format(url))


def download_pages(items):
    retry = 0
    while retry < 10:
        pool = ThreadPool(4)
        try:
            pool.map(download_page, items)
            pool.close()
            pool.join()
            break
        except KeyboardInterrupt:
            print('download terminated by user, quit execution.')
            pool.terminate()
            break
        except Exception, e:
            pool.terminate()
            retry += 1
            print('download error occurred: {0}, {1} retry in {2}s'.format(
                e, retry, retry * 10))
            time.sleep(retry * 10)

    # for item in items:
    #     download_page(item)


def url_to_item(link):
    item = {}
    item['text'] = link.text
    item['href'] = link.get('href')
    item['date'] = re.compile(url_date_pat).search(item['text']).group(1)
    item['id'] = re.compile(url_id_pat).search(item['href']).group(1)
    return item


def fetch_or_load_urls(fileanme):
    if os.path.exists(jsonfile):
        return json.load(open(jsonfile, 'r'))
    pool = ThreadPool(8)
    try:
        pool.map(findurls, range(1, 51))
        pool.close()
        pool.join()

    except KeyboardInterrupt:
        print('terminated by user.')
        pool.terminate()

    print(len(urls))

    items = [url_to_item(url) for url in sorted(urls, cmp=url_cmp)]
    # json.dump(items, open('urls.json', 'w'),indent=2) # 输出\uxxxx
    json.dump(items, codecs.open(fileanme, 'w', 'utf8'),  # 输出中文文字
              ensure_ascii=False, indent=2)

    return items

if __name__ == '__main__':
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)
    jsonfile = os.path.join(OUTPUT, 'penti.json')
    items = fetch_or_load_urls(jsonfile)
    download_pages(items)
