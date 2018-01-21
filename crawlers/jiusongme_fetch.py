#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-17 11:31:14
from __future__ import print_function
import codecs
import requests
import base64
import json
import sys
import os
import time
import shutil
import random
import commons
import argparse
import traceback
import zhconv
import utils
from bs4 import BeautifulSoup
from utils import read_list, write_list, distinct_list, unquote_url

ENC_ROOT_URL = 'aHR0cHM6Ly85c29uZy5tZS8='
OUTPUT = 'ninesong'


def get_root_url():
    return base64.b64decode(ENC_ROOT_URL)


def filter_post_content(tag):
    return tag.name == 'div' and tag.get('class') == ['entry-inner']


def filter_post_url(tag):
    return (tag.name == 'a' and tag.get('href') and
            tag.text and tag.parent and
            tag.parent.get('class') == ['post-title', 'entry-title'])


def fetch_post(url, output=os.path.join(OUTPUT, 'posts')):
    if not os.path.exists(output):
        os.makedirs(output)
    post_name = zhconv.convert(utils.url_filename(url), 'zh-cn')
    post_file = os.path.join(output, '%s.txt' % post_name)
    if os.path.exists(post_file):
        print('Skip %s' % url)
    else:
        print('Fetch %s' % url)
        soup = commons.soup(url, encoding='utf8')
        for s in soup.find_all('a'):
            s.decompose()
        content = soup.find(filter_post_content)
        content = zhconv.convert(content.get_text(), 'zh-cn')
        # print('Post %s (%s)' % (post_name, len(content)))
        if content and len(content) > 500:
            with codecs.open(post_file, 'w', 'utf-8') as f:
                f.write(post_name)
                f.write('\n\n')
                f.write(content)


def fetch_all_posts(use_pool=False):
    print('Fetch all posts use_pool=%s' % use_pool)
    output = OUTPUT
    list_file = os.path.join(output, 'all.txt')
    urls = read_list(list_file) or []
    if use_pool:
        commons.MultiTask(fetch_post, urls).start()
    else:
        for url in urls:
            fetch_post(url)
            time.sleep(random.randint(0, 2))


def fetch_page_urls(page_no):
    url = '%spage/%s/' % (get_root_url(), page_no)
    print('fetch page %s' % url)
    soup = commons.soup(url, encoding='utf8')
    tags = soup.find_all(filter_post_url)
    return [t.get('href') for t in tags]
    # fetch_post(links[0])


def fetch_all_urls(start=0, end=5, delta=True):
    output = OUTPUT
    list_file = os.path.join(output, 'all.txt')
    all_urls = read_list(list_file) or []
    pl_output = os.path.join(output, 'list')
    if not os.path.exists(pl_output):
        os.makedirs(pl_output)
    pl_name_tpl = 'jiusong_p_%s.txt'
    not_found_count = 0
    for i in range(start, end):
        pl_file = os.path.join(pl_output, pl_name_tpl % i)
        if delta and os.path.exists(pl_file):
            print('Skip exist page %s' % i)
            continue
        try:
            urls = fetch_page_urls(i)
            if urls:
                all_urls.extend(urls)
                write_list(pl_file, fix_urls(urls))
            time.sleep(random.randint(0, 2))
        except KeyboardInterrupt, e:
            print("User interrupt, quit.")
            raise
        except Exception, e:
            print("Error:'%s' on fetch page %s" % (e, i))
            # traceback.print_exc()
            error_count += 1
            if error_count > 10:
                traceback.print_exc()
                break
            time.sleep(5)
        finally:
            write_list(list_file, fix_urls(all_urls))


def fix_urls(urls):
    urls = distinct_list(urls, sort=True, reverse=True)
    return [unquote_url(url) for url in urls]


def fix_list_file():
    output = OUTPUT
    list_file = os.path.join(output, 'all.txt')
    all_urls = read_list(list_file) or []
    all_urls = [unquote_url(url) for url in all_urls]
    write_list(list_file, all_urls)


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: %s -r[recent] or -a[all] or -d[download]' % sys.argv[0])
        exit(1)
    if sys.argv[1] == '-r':
        # recent
        fetch_all_urls(1, 10, delta=False)
    elif sys.argv[1] == '-a':
        # all
        fetch_all_urls(1, 1000, delta=False)
    elif sys.argv[1] == '-d':
        fetch_all_posts(use_pool=True)


if __name__ == '__main__':
    # fix for relative import other script
    # https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # print(sys.path)
    main()
