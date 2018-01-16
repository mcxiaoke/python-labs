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
from utils import read_list, write_list

ENC_ROOT_URL = 'aHR0cHM6Ly85c29uZy5tZS8='


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


def fetch_page(page_no):
    url = '%spage/%s/' % (get_root_url(), page_no)
    print('fetch page %s' % url)
    soup = commons.soup(url, encoding='utf8')
    tags = soup.find_all(filter_post_url)
    return [t.get('href') for t in tags]
    # fetch_post(links[0])

def fetch_all(total):
    list_file = 'jiusong_all.txt'
    page_file = 'jiusong_p_%s.txt'
    all_urls = []
    for i in range(1,total):
        try:
            urls = fetch_page(i)
            if urls:
                all_urls.extend(urls)
                write_list(page_file % i, urls)
            time.sleep(random.randint(1, 2))
        except KeyboardInterrupt, e:
            print("User interrupt, quit.")
            raise
        except Exception, e:
            print("Error:%s On fetch page %s" % (e, i))
            traceback.print_exc()
            time.sleep(10)
        finally:
            write_list(list_file, all_urls)     

def main():
    fetch_all(405)

if __name__ == '__main__':
    main()
