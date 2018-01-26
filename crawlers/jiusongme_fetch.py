#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-17 11:31:14
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import requests
import base64
import json
import sys
import os
import re
import time
import shutil
import random
import argparse
import traceback
import zhconv

ENC_ROOT_URL = 'aHR0cHM6Ly85c29uZy5tZS8='
OUTPUT = 'output-jiusong'


def get_root_url():
    return compat.to_text(base64.b64decode(ENC_ROOT_URL))

def filter_post_content(tag):
    return tag.name == 'div' and tag.get('class') == ['entry-inner']


def filter_post_url(tag):
    return (tag.name == 'a' and tag.get('href') and
            tag.text and tag.parent and
            tag.parent.get('class') == ['post-title', 'entry-title'])


def fetch_post(url, output=os.path.join(OUTPUT, 'posts')):
    if not os.path.exists(output):
        os.makedirs(output)
    post_name = zhconv.convert(url_filename(url), 'zh-cn')
    post_file = os.path.join(output, '%s.txt' % post_name)
    if os.path.exists(post_file):
        print('Skip %s' % url)
    else:
        print('Fetch %s' % url)
        soup = commons.soup(url)
        for s in soup.find_all('a'):
            s.decompose()
        content_tag = soup.find(filter_post_content)
        content = content_tag.get_text()
        # print('Post %s (%s)' % (post_name, len(content)))
        if content and len(content) > 500:
            content = re.sub(r'[><&%]','',content)
            content = zhconv.convert(content, 'zh-cn')
            with codecs.open(post_file, 'w', 'utf-8') as f:
                f.write(post_name)
                f.write('\n\n')
                f.write(content)


def fetch_all_posts(use_pool=True, max_count=999999,
                    list_file=None, output=OUTPUT):
    print('Fetch all posts use_pool=%s' % use_pool)
    output = output or OUTPUT
    list_file = list_file or os.path.join(output, 'all.txt')
    urls = read_list(list_file) or []
    urls = urls[:max_count]
    if use_pool:
        commons.run_in_pool(fetch_post, urls)
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


def fetch_all_urls(start=0, end=5, list_file=None, output=OUTPUT):
    output = output or OUTPUT
    list_file = list_file or os.path.join(output, 'all.txt')
    all_urls = read_list(list_file) or []
    pl_output = os.path.join(output, 'list')
    if not os.path.exists(pl_output):
        os.makedirs(pl_output)
    new_urls = commons.run_in_pool(fetch_page_urls, range(start, end))
    if new_urls:
        new_urls = flatten_list(new_urls)
        print('fetch %s new urls' % len(new_urls))
        all_urls.extend(new_urls)
        write_list(list_file, fix_urls(all_urls))
        new_list_file = os.path.join(output, 'new_%s_%s.txt' % (start, end))
        write_list(new_list_file, fix_urls(new_urls))


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
    if sys.argv[1] == '-0':
        # recent
        fetch_all_urls(1, 4)
    elif sys.argv[1] == '-r':
        # recent
        fetch_all_urls(1, 11)
    elif sys.argv[1] == '-a':
        # all
        fetch_all_urls(1, 1000)
    elif sys.argv[1] == '-dr':
        fetch_all_posts(max_count=200)
    elif sys.argv[1] == '-da':
        fetch_all_posts()
    else:
        print('Usage: %s -r[recent] or -a[all] or -d[download]' % sys.argv[0])
        exit(1)


if __name__ == '__main__':
    # fix for relative import other script
    # https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    # print(sys.path)
    from lib import compat, commons
    from lib.utils import read_list, write_list, distinct_list, flatten_list, unquote_url, url_filename
    main()
