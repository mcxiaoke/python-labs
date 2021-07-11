'''
File: weather_pics.py
Created: 2021-07-11 16:04:11
Modified: 2021-07-11 16:04:15
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''

import os
import sys
import requests
import shutil
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

LOG_FILE = 'weather_pics_log.txt'
PAGE_URL = 'http://www.weather.com.cn/index/zxqxgg1/new_wlstyb.shtml'
RAIN_IMG_PATTERN = 'pi.weather.com.cn/i/product/xml/sevp_nmc_webu_'


def filter_rain_image(tag):
    return tag.name == 'img' and tag.parent.name == 'a' and tag.attrs and tag.attrs['src'] and RAIN_IMG_PATTERN in tag.attrs['src']


def parse_urls():
    res = requests.get(PAGE_URL, headers={'User-Agent': USER_AGENT})
    res.encoding = 'utf-8'
    if res.ok:
        content = res.text
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all(filter_rain_image)
        return [link.attrs['src'] for link in links]


def download_one(url, output='.'):
    filename = url.split('/')[-1]
    filename = filename.split('_')[-1]
    r = requests.get(url, stream=True, headers={
        'User-Agent': USER_AGENT})
    length = int(r.headers['Content-length'])
    print(r.status_code, length)
    if r.ok and length > 20*1000:
        print('Downloading {}'.format(url))
        save_path = os.path.join(output, filename)
        save_path = os.path.abspath(save_path)
        if os.path.exists(save_path):
            print('Skip {}'.format(save_path))
            return
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print('Saved to {}'.format(save_path))
            return save_path


def download_urls(output='.'):
    print('Output: {}'.format(os.path.abspath(output)))
    urls = parse_urls()
    for url in urls:
        download_one(url, output)


if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else '.'
    download_urls(output)
