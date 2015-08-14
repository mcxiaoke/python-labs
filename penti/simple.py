#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 08:35:05
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import os
import sys
import codecs
import Queue as queue
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
import json

OUTPUT = 'output'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
           'Referer': 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei'}

url_tpl = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei&page={0}'  # page
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
    r = requests.get(url, timeout=10)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(myurl)
    if links:
        print('fetch page ' + str(page) + 'found links ' + str(len(links)))
        lock.acquire()
        urls.extend(links)
        lock.release()
    return links


def download_and_save(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)


def download_page(item):
    charset_pat = re.compile(r'charset=(gb2312)')
    id = item['id']
    url = page_tpl.format(id)
    r = requests.get(url, timeout=20)
    # 必须用gbk，要不然繁体乱码
    # 虽然网页上写的是gb2312，但是浏览器实际使用的是gbk
    r.encoding = 'gbk'
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')

    imgs = soup.find_all('img')

    imgdir = os.path.join(OUTPUT, 'images')
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)

    for img in imgs:
        from_src = img['src']
        if not from_src.startswith('http://'):
            from_src = 'http://www.dapenti.com/blog/{0}'.format(from_src)
        to_src = from_src.replace('/', '_').replace(':', 'x')
        imgfile = os.path.join(imgdir, to_src)
        img['src'] = os.path.join('images', to_src)
        if os.path.exists(imgfile):
            print('image exists, skip {0}'.format(from_src))
        else:
            print('download image {0}'.format(from_src))
            download_and_save(from_src, imgfile)

    filename = os.path.join(OUTPUT, '{}.html'.format(id))
    with open(filename, 'w') as f:
        # 用utf写入文件，所以html头的gb2312需要改为utf8
        content = unicode(soup).replace('gb2312', 'utf-8')
        f.write(content.encode('utf8'))
    print('page saved to {0}'.format(filename))


def url_to_item(link):
    item = {}
    item['text'] = link.text
    item['href'] = link.get('href')
    item['date'] = re.compile(url_date_pat).search(item['text']).group(1)
    item['id'] = re.compile(url_id_pat).search(item['href']).group(1)
    return item

if __name__ == '__main__':
    pool = ThreadPool(8)
    try:
        pool.map(findurls, range(1, 2))
        pool.close()
        pool.join()

    except KeyboardInterrupt:
        pool.terminate()

    print(len(urls))

    items = [url_to_item(url) for url in sorted(urls, cmp=url_cmp)]
    # json.dump(items, open('urls.json', 'w'),indent=2) # 输出\uxxxx
    json.dump(items, codecs.open('urls.json', 'w', 'utf8'),  # 输出中文文字
              ensure_ascii=False, indent=2)

    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)

    download_page(items[1])
    # pool = ThreadPool(8)
    # try:
    #     pool.map(download_page, items)
    #     pool.close()
    #     pool.join()
    # except KeyboardInterrupt:
    #     pool.terminate()

    # data = json.load(open('urls.json', 'r'))
    # for d in data:
    #     print(d['text'].encode('utf8'))
