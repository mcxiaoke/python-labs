from __future__ import print_function, unicode_literals
import codecs
import base64
import json
import sys
import os
import re
import time
import shutil
import random
import requests
import bs4
import urlparse

sys.path.insert(1, os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
from lib import commons
from lib import utils

from bs4 import BeautifulSoup
 
def strip_html(html_string):
    soup = BeautifulSoup(html_string, 'html5lib')
    print(soup)
    text = soup.find_all(text=lambda text:isinstance(text, bs4.element.NavigableString))
    return " ".join(text)

def print_css_links(url):
    soup = commons.soup(url)
    raw_css_urls = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
    css_urls = [u'https:%s' % url if url.startswith(u'//') else url for url in raw_css_urls]

def main2():
    # print_css_links(u'https://www.douban.com/note/645097084/')
    r = commons.get('https://baike.baidu.com/item/%E7%8C%AB%E5%92%AA')
    # r = commons.get('https://www.douban.com/note/645097084/')
    print(r.encoding)
    print(r.apparent_encoding)
    print(requests.utils.get_encodings_from_content(r.content))
    print(type(r.text))
    print(r.text[:300])

def main():
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        for line in lines:
            print(line)
            print('-------')



def strip_html_tags():
    with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
        print(strip_html(f.read()))

if __name__ == '__main__':
    strip_html_tags()
