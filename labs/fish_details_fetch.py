#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
from __future__ import print_function
import codecs
import os
import sys
import shutil
import re
from bs4 import BeautifulSoup
import commons

LS_URL = u'http://zgdwz.lifescience.com.cn/ashx/searchinfo.ashx?key={}'
LS_INFO_URL = u'http://zgdwz.lifescience.com.cn/info/{}'
BD_URL = u'https://baike.baidu.com/item/{}'
BD_HOST = u'https://baike.baidu.com'
HD_URL = u'http://www.baike.com/wiki/{}'
ZO_URL = u'http://zgdwz.lifescience.com.cn/search?key={}&t=2'
ZO_HOST = u'http://zgdwz.lifescience.com.cn'
CSDB_URL = u'http://www.zoology.csdb.cn/efauna/searchTaxon?search={}'
CSDB_HOST = u'http://www.zoology.csdb.cn/efauna/'

'''
curl 'http://zgdwz.lifescience.com.cn/ashx/autocomplete.ashx?q=%E9%A9%AC%E5%8F%A3&limit=20&timestamp=1514366731531' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,de;q=0.5,fr;q=0.4,pl;q=0.3,pt;q=0.2,es;q=0.1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: http://zgdwz.lifescience.com.cn/search?key=%E9%A9%AC%E5%8F%A3%E9%B1%BC&t=2' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed
'''


def clean_text(text, minlen=300):
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r' {2,}', ' ', text)
    if len(text) < minlen:
        return None
    return text


def parse_ls_text(html):
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup('style'):
        s.decompose()
    for s in soup.find_all(class_='ipvip'):
        s.decompose()
    s = soup.find('div', id='centerdiv')
    title = soup.title.get_text().strip()
    content = clean_text(s.get_text('\n')) if s else None
    return title, content


def parse_bd_text(html):
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup('style'):
        s.decompose()
    s = soup.find('div', class_='main-content')
    return clean_text(s.get_text('\n')) if s else None


def parse_hd_text(html):
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup('style'):
        s.decompose()
    for s in soup.select('#index-footer'):
        s.decompose()
    for s in soup.find_all(class_='wap-citiao'):
        s.decompose()
    for s in soup.find_all(class_='bjbd'):
        s.decompose()
    s = soup.find(id='content')
    return clean_text(s.get_text('\n')) if s else None


def parse_csdb_text(html):
    soup = BeautifulSoup(html, "lxml")
    for s in soup('script'):
        s.decompose()
    for s in soup('style'):
        s.decompose()
    return clean_text(soup.get_text('\n')) if s else None


def csdb_info_link(tag):
    return not tag.has_attr('class') \
        and tag.has_attr('href') \
        and tag['href'].startswith('getTaxon') \



def get_csdb_url(name):
    exclude = [u'属', u'科', u'目', u'蚊', u'蛾', u'虫']
    r = commons.get(CSDB_URL.format(name), encoding='utf-8',
                    allow_redirects=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        result = None
        for s in soup.find_all(csdb_info_link):
            skip = False
            for e in exclude:
                if e in s.text:
                    skip = True
                    break
            if skip:
                continue
            if name in s.text:
                result = s['href']
                break
        if result:
            return CSDB_HOST + result


def download_csdb_info(name, dst):
    ofile = os.path.join(dst, u"{}_csdb.txt".format(name))
    if os.path.exists(ofile):
        print(u'CSDB Skip {}'.format(name))
        return ofile
    csdb_url = get_csdb_url(name)
    csdb_text = None
    if csdb_url:
        r = commons.get(csdb_url, encoding='utf-8',
                        allow_redirects=False)
        if r.status_code == 200:
            csdb_text = parse_csdb_text(r.text)
    if csdb_text:
        with codecs.open(ofile, 'w', 'utf-8') as f:
            print(u'CSDB Found {}'.format(name))
            f.write(csdb_url)
            f.write('\n\n')
            f.write(csdb_text)
            return ofile


def download_bd_info(name, dst):
    ofile = os.path.join(dst, u"{}_bd.txt".format(name))
    if os.path.exists(ofile):
        print(u'Baidu Skip {}'.format(name))
        return ofile
    bd_url = BD_URL.format(name)
    bd_text = None
    r = commons.get(bd_url, encoding='utf-8',
                    allow_redirects=False)
    if r.status_code == 200:
        bd_text = parse_bd_text(r.text)
    elif r.status_code == 302:
        location = r.headers['Location']
        if location and location.startswith('/item/'):
            bd_url = "{}{}".format(BD_HOST, location)
            r = commons.get(bd_url, encoding='utf-8',
                            allow_redirects=False)
            if r.status_code == 200:
                bd_text = parse_bd_text(r.text)
    else:
        if name.endswith(u'鱼'):
            bd_url = BD_URL.format(name[:-1])
            r = commons.get(bd_url, encoding='utf-8',
                            allow_redirects=False)
            if r.status_code == 200:
                bd_text = parse_bd_text(r.text)
    if bd_text:
        with codecs.open(ofile, 'w', 'utf-8') as f:
            print(u'Baidu Found {}'.format(name))
            f.write(bd_url)
            f.write('\n\n')
            f.write(bd_text)
            return ofile


def download_hd_info(name, dst):
    ofile = os.path.join(dst, u"{}_hd.txt".format(name))
    if os.path.exists(ofile):
        print(u'Hudong Skip {}'.format(name))
        return ofile
    hd_url = HD_URL.format(name)
    hd_text = None
    r = commons.get(hd_url, encoding='utf-8',
                    allow_redirects=False)
    if r.status_code == 200:
        hd_text = parse_hd_text(r.text)
    if hd_text:
        with codecs.open(ofile, 'w', 'utf-8') as f:
            print(u'Hudong Found {}'.format(name))
            f.write(hd_url)
            f.write('\n\n')
            f.write(hd_text)
            return ofile


def download_info(name, dst):
    print(u'Processing {}'.format(name))
    a = download_csdb_info(name, dst)
    b = download_bd_info(name, dst)
    c = download_hd_info(name, dst)
    return a or b or c


def download_fish_list(list_file, dst=None):
    if not dst:
        dst = os.path.dirname(list_file)
    names = codecs.open(list_file, 'r', encoding='utf-8').read().splitlines()
    for name in names:
        url = LS_URL.format(name)
        r = commons.get(url, encoding='utf-8', allow_redirects=False)
        if r.status_code != 200:
            continue
        if not r.text:
            continue
        url = LS_INFO_URL.format(r.text)
        r = commons.get(url, encoding='utf-8',
                        allow_redirects=False)
        if r.status_code != 200:
            continue
        title, content = parse_ls_text(r.text)
        if title and content:
            ofile = os.path.join(dst, u'{}.txt'.format(title))
            with codecs.open(ofile, 'w', 'utf-8') as f:
                print(u'Saved {}'.format(title))
                f.write(content)


def main(list_file, dst=None):
    if not dst:
        dst = os.path.dirname(list_file)
    nt_file = os.path.join(dst, "notfound.txt")
    names = codecs.open(list_file, 'r', encoding='utf-8').read().splitlines()
    nt_names = []
    for name in names:
        if not download_info(name, dst):
            nt_names.append(name)
    with codecs.open(nt_file, 'w', 'utf-8') as f:
        f.write('\n'.join(nt_names))


if __name__ == '__main__':
    if True:
        download_fish_list(os.path.abspath(sys.argv[1]))
        sys.exit(0)
    if len(sys.argv) < 2:
        print('Usage: {} list.txt'.format(sys.argv[0]))
        sys.exit(1)
    list_file = os.path.abspath(sys.argv[1])
    if len(sys.argv) > 2:
        dst = os.path.abspath(sys.argv[2])
    else:
        dst = os.path.dirname(list_file)
    main(list_file, dst)
