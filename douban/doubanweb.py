# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-28 11:14:26
# @Last Modified by:   mcxiaoke
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import requests
import cookielib
import base64
import json
import sys
import os
import re
import time
import shutil
import urllib
import pickle
import random
import argparse
import traceback
import pprint
import logging
import subprocess
from lxml import etree, html
from requests.exceptions import HTTPError
from doubanapi import COUNT
logger = logging.getLogger('doubanweb')

sys.path.insert(1, os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
from lib.compat import raw_input
from lib.utils import write_file


USER_AGENT_OSX = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0'

DOUBAN_URL = 'https://www.douban.com'
LOGIN_URL = 'https://www.douban.com/accounts/login'
USER_ALBUMS_PAGE_URL = 'https://www.douban.com/people/%s/photos?start=%s'
DOULIST_PAGE_URL = 'http://www.douban.com/doulist/%s/?sort=time&sub_type=12&start=%s'

COUNT_IN_DOULIST_PAGE = 25
RE_ALBUM_URL_ID = re.compile(r'/photos/album/(\d+)/?')
RE_DOULIST_URL_ID = re.compile(r'/doulist/(\d+)/?')
RE_USER_URL_ID = re.compile(r'/people/(\d+)/?')

_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': USER_AGENT_OSX,
    'Referer': DOUBAN_URL
}

_session = requests.Session()
_session.headers.update(_headers)
#_cookie_file = os.path.join(os.path.expanduser('~'),'.douban.cookie.txt')
cookie_file = os.path.join(os.path.expanduser('~'), '.douban.cookie.dat')
#cookie = cookielib.LWPCookieJar(filename=_cookie_file)


def load_cookies():
    if os.path.exists(cookie_file):
        with open(cookie_file) as f:
            _session.cookies = requests.utils.cookiejar_from_dict(
                pickle.load(f))


def save_cookies():
    with open(cookie_file, 'w') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(_session.cookies), f)


def check_login():
    load_cookies()
    if not _session.cookies:
        login()


def parse_captcha(text):
    root = etree.HTML(text)
    captcha_image = root.xpath('//img[@id="captcha_image"]/@src')
    captcha_id = root.xpath('//input[@name="captcha-id"]/@value')
    if captcha_image and captcha_id:
        return (captcha_image[0], (captcha_id[0]))


def login():
    print('Please login before operations:')
    username = raw_input('Username: ')
    password = raw_input('Password: ')
    r1 = _get(DOUBAN_URL)
    text = r1.text
    write_file('login-before.html', text)
    data = {
        'source': 'index_nav',
        'redir': DOUBAN_URL,
        'remember': 'on',
        'login': '登录',
        'form_email': username,
        'form_password': password
    }
    t = parse_captcha(text)
    if t:
        captcha_image, captcha_id = t
    else:
        captcha_image = None
        captcha_id = None
    captcha_value = None
    if captcha_image and captcha_id:
        print('login need captcha %s' % captcha_image)
        urllib.urlretrieve(captcha_image, filename='captcha.png')
        subprocess.call(['open', 'captcha.png'])
        captcha_value = raw_input('Captcha: ')
        if captcha_value:
            data['captcha-solution'] = captcha_value
            data['captcha-id'] = captcha_id
    r = _post(LOGIN_URL, data=data)
    root = etree.HTML(r.text)
    if root.xpath('//div[@id="statuses"]'):
        save_cookies()
        print('Login successful!!!')
    print(r.headers)
    print(requests.utils.dict_from_cookiejar(_session.cookies))
    write_file('login-after.html', r.text)


def _request(method, url, **kwargs):
    cookie = requests.utils.dict_from_cookiejar(_session.cookies)
    logger.debug('_request: %s %s %s' % (method, url, cookie))
    r = _session.request(method, url, timeout=30, **kwargs)
    r.encoding = 'utf-8'
    if r.status_code >= 400:
        logger.error('_response: %s %s %s' % (method, url, r.status_code))
        raise HTTPError(response=r)
    return r


def _get(url, encoding=None, **kwargs):
    return _request('get', url, **kwargs)


def _post(url, encoding=None, **kwargs):
    return _request('post', url, **kwargs)


def _get_albums_in_page(url):
    root = etree.HTML(_get(url).text)
    links = root.xpath(
        '//div[@class="title"]/a[contains(@href,"/photos/album/")]')
    # (url, title)
    return [(l.attrib['href'], l.text.strip()) for l in links]


def get_id_from_album_url(url):
    # https://www.douban.com/photos/album/1625987334/
    m = re.search(RE_ALBUM_URL_ID, url)
    return m.group(1) if m else None


def get_id_from_doulist_url(url):
    # https://www.douban.com/doulist/1798107/
    m = re.search(RE_DOULIST_URL_ID, url)
    return m.group(1) if m else None

def get_id_from_user_url(url):
    # https://www.douban.com/people/doiv/
    m = re.search(RE_USER_URL_ID, url)
    return m.group(1) if m else None

def get_albums_in_doulist(doulist_id, max_page=9999):
    logger.debug('get_albums_in_doulist doulist_id=%s max_page=%s'
                 % (doulist_id, max_page))
    albums = []
    page_no = 0
    start = 0
    while page_no < max_page:
        page_no += 1
        page_url = DOULIST_PAGE_URL % (doulist_id, start)
        logger.info('get_albums_in_doulist processing %s' % page_url)
        try:
            new_albums = _get_albums_in_page(page_url)
        except HTTPError as e:
            logger.error('get_albums_in_doulist error %s' % e)
            logger.warning('get_albums_in_doulist [%s]' % e.response.text)
            new_albums = []
            if e.response.status_code == 404:
                # doulist has been deleted
                albums = []
                return None
        if not new_albums:
            break
        logger.info('get_albums_in_doulist found %s new albums in doulist %s'
                    % (len(new_albums), doulist_id))
        albums.extend(new_albums)
        start += COUNT_IN_DOULIST_PAGE
        if len(new_albums) < COUNT_IN_DOULIST_PAGE / 2:
            break
        time.sleep(random.randint(0, 5))
    logger.info('get_albums_in_doulist found %s albums in doulist %s' %
                (len(albums), doulist_id))
    return albums


def get_album_ids_in_doulist(doulist_id, max_page=9999):
    albums = get_albums_in_doulist(doulist_id, max_page)
    return [get_id_from_album_url(url) for url, _ in urls]


check_login()

if __name__ == '__main__':
    login()
    # albums = get_albums_in_doulist('2618868')
    # for url,title in albums:
    #     print('%s - %s' % (url, title))
