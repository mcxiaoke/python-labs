#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 08:35:05
from __future__ import print_function
from bs4 import BeautifulSoup
from requests import exceptions
import re
import os
import sys
import codecs
import time
import Queue as queue
import signal
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool
import json
import shutil
from lib import commons

'''
喷嚏网 - 喷嚏图卦图文下载，替换图片链接为本地图片
'''
# 保存目录
OUTPUT = 'output-penti-pages'

# 列表分页URL
url_tpl = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei&page={0}'
# 某一篇喷嚏图卦的页面URL
page_tpl = 'http://www.dapenti.com/blog/more.asp?name=xilei&id={0}'

urls = []
lock = Lock()

url_date_pat = re.compile(u'【\S+(\d{8})】')  # 匹配日期
url_id_pat = re.compile(u'&id=(\d+)')  # 匹配ID

# 提取URL文本中的日期信息，用于比较排序


def url_cmp(ua, ub):
    a = url_date_pat.search(ua.text).group(1)
    b = url_date_pat.search(ub.text).group(1)
    # print(a.encode('utf8'),b.encode('utf8'))
    return cmp(b, a)

# 匹配列表页中图卦的URL


def filter_page_url(a):
    return (a.get('href') and a.text and
            a.parent.name == 'li' and
            re.compile(u'\S+图卦\d{8}】.+').search(a.text))

# 找到某个列表页全部的图卦URL


def find_all_tugua_urls(page):
    url = url_tpl.format(page)
    print('fetch {0}'.format(url))
    soup = commons.soup(url, encoding='gbk')
    links = soup.find_all(filter_page_url)
    if links:
        print('fetch {0} urls in page {1}'.format(len(links), page))
        lock.acquire()
        urls.extend(links)
        lock.release()
    return links

# 针对某些CDN地址的修复


def fix_img_url(url):
    url = url.replace('imgs.dapenti.org:88', 'ptimg.org:88')
    url = url.replace('imgs.dapenti2.com:88', 'ptimg.org:88')
    return url


# 下载某个图片URL，保存为文件
def download_image(url, filename, id):
    url = fix_img_url(url)
    print('download image for {0}: {1}'.format(id, url))
    return commons.download_file(url, filename)

# 下载某一期的图卦正文和图片


def download_page(item):
    id = item['id']
    url = page_tpl.format(id)
    # 如果已下载，跳过
    filename = os.path.join(OUTPUT, '{}.html'.format(id))
    if os.path.exists(filename):
        print('skip page {0}'.format(url))
        return
    print('download page: {0}'.format(url))
    # 必须用gbk，要不然繁体乱码
    # 虽然网页上写的是gb2312，但是浏览器实际使用的是gbk
    soup = commons.soup(url, encoding='gbk')
    # 获取所有的图片URL
    imgs = soup.find_all('img')
    # 图片保存目录
    img_dirname = 'images_{0}'.format(id)
    imgdir = os.path.join(OUTPUT, img_dirname)
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    # 逐个下载图片
    for img in imgs:
        from_src = img['src']
        # 跳过没有扩展名的图片
        if not os.path.splitext(from_src)[1]:
            continue
        if not from_src.startswith('http://'):
            # 给部分不是完整的图片URL添加域名部分
            from_src = 'http://www.dapenti.com/blog/{0}'.format(from_src)
        # 过滤不合法的文件名字符
        to_src = commons.get_safe_filename(from_src)
        imgfile = os.path.join(imgdir, to_src)
        # 替换为本地图片链接
        img['src'] = os.path.join(img_dirname, to_src)
        if os.path.exists(imgfile):
            # 跳过已存在的图片
            print('skip exists image {0}'.format(from_src))
        else:
            # 不存在则下载
            iurl, iname = download_image(from_src, imgfile, id)
            if not iname:
                # 如果图片无法下载，保留原始URL
                img['src'] = from_src
    tempfile = '{0}.tmp'.format(filename)
    # 如果正文和图片都下载完成，没有错误，则保存到文件
    with open(tempfile, 'w') as f:
        # 用utf写入文件，所以html头的gb2312需要改为utf8
        content = unicode(soup).replace('charset=gb2312', 'charset=utf-8')
        f.write(content.encode('utf8'))
    commons.safe_rename(tempfile, filename)
    print('page saved {0}'.format(url))


def download_pages(items):
    # 多进程/线程下载全部图卦
    retry = 0
    while retry < 10:
        pool = ThreadPool(4)
        try:
            pool.map(download_page, items)
            pool.close()
            pool.join()
            break
        except KeyboardInterrupt, e:
            print('download terminated by user, quit now.', e)
            pool.terminate()
            pool.join()
            break
        except (IOError, OSError), e:
            pool.terminate()
            pool.join()
            retry += 1
            print('download error: {0}, {1} retry in {2}s'.format(
                e, retry, retry * 10))
            time.sleep(retry * 10)

    # for item in items:
    #     download_page(item)


def url_to_item(link):
    # 将a标签转换为JSON数据结构
    item = {}
    item['text'] = link.text
    item['href'] = link.get('href')
    item['date'] = re.compile(url_date_pat).search(item['text']).group(1)
    item['id'] = re.compile(url_id_pat).search(item['href']).group(1)
    return item


def fetch_or_load_urls(filename):
    # 获取全部的图卦URL列表
    # 如果存在缓存，从缓存读取
    # 否则从网上多线程/进程获取
    if os.path.exists(jsonfile):
        print('found url json file cache {0}'.format(filename))
        return json.load(open(jsonfile, 'r'))
    pool = ThreadPool(4)
    try:
        pool.map(find_all_tugua_urls, range(1, 51))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print('terminated by user.')
        pool.terminate()
        pool.join()

    items = [url_to_item(url) for url in sorted(urls, cmp=url_cmp)]

    if items:
        # json.dump(items, open('urls.json', 'w'),indent=2) # 输出\uxxxx
        json.dump(items, codecs.open(filename, 'w', 'utf8'),  # 输出中文文字
                  ensure_ascii=False, indent=2)

        print('saved url json file cache to {0}'.format(filename))
    else:
        print('no url items found, maybe something wrong!')

    return items

if __name__ == '__main__':
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)
    jsonfile = os.path.join(OUTPUT, 'penti.json')
    items = fetch_or_load_urls(jsonfile)
    if items:
        print('{0} urls found'.format(len(items)))
        download_pages(items)
        # for item in items:
            # download_page(item)
    else:
        print('no urls ,exit')
