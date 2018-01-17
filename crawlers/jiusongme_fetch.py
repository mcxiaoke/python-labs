# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-16 16:39:00
# @Last Modified by:   mcxiaoke
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
from bs4 import BeautifulSoup
from utils import read_list, write_list, distinct_list,unquote_url

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


def fetch_post(url):
    print('fetch post %s' % url)
    soup = commons.soup(url, encoding='utf8')
    for s in soup.find_all('a'):
        s.decompose()
    content = soup.find(filter_post_content)
    text = zhconv.convert(content.get_text(), 'zh-cn')
    print(text)


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
    pl_output = os.path.join(output,'list')
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
    # recent
    fetch_all_urls(1, 10, delta=False)
    # all
    # fetch_all_urls(1, 1000, delta=False)
    # fix_list_file()


if __name__ == '__main__':
    main()
