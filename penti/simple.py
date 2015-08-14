#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 08:35:05
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import codecs
import Queue as queue
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
import json

url_tpl = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei&page={0}'

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
    r = requests.get(url)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(myurl)
    if links:
        print('fetch page ' + str(page) + 'found links ' + str(len(links)))
        lock.acquire()
        urls.extend(links)
        lock.release()
    return links


def url_to_item(link):
    item = {}
    item['text'] = link.text
    item['href'] = link.get('href')
    item['date'] = re.compile(url_date_pat).search(item['text']).group(1)
    item['id'] = re.compile(url_id_pat).search(item['href']).group(1)
    return item

if __name__ == '__main__':
    try:
        pool = ThreadPool(8)
        pool.map(findurls, range(1, 60))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()

    print(len(urls))

    items = [url_to_item(url) for url in sorted(urls, cmp=url_cmp)]
    # json.dump(items, open('urls.json', 'w'),indent=2) # 输出\uxxxx
    json.dump(items, codecs.open('urls.json', 'w', 'utf8'),  # 输出中文文字
              ensure_ascii=False, indent=2)
    # data = json.load(open('urls.json', 'r'))
    # for d in data:
    #     print(d['text'].encode('utf8'))
