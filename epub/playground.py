from __future__ import print_function
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

def print_css_links(url):
    soup = commons.soup(url)
    raw_css_urls = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
    css_urls = [u'https:%s' % url if url.startswith(u'//') else url for url in raw_css_urls]

def main():
    # print_css_links(u'https://www.douban.com/note/645097084/')
    r = commons.get('https://baike.baidu.com/item/%E7%8C%AB%E5%92%AA')
    # r = commons.get('https://www.douban.com/note/645097084/')
    print(r.encoding)
    print(r.apparent_encoding)
    print(requests.utils.get_encodings_from_content(r.content))
    print(type(r.text))
    print(r.text[:300])

if __name__ == '__main__':
    main()