#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-21 23:01:03

'''
data sample

curl 'http://v2ex.com/signin' -H 'Cookie: _ga=GA1.2.1489776380.1426669813; V2EX_REFERRER="2|1:0|10:1440045150|13:V2EX_REFERRER|16:YXByaWt5Ymx1ZQ==|db8460a2be8edeacf5c63181d48419887af915d6c6c0acac639a3e8d31390462"; PB3_SESSION="2|1:0|10:1440162388|11:PB3_SESSION|36:djJleDoyMjIuMTg3LjAuNjY6NjI5MjQzOTg=|dd1a45a26d9124d9eb907cafbe12905940eee9f20d0fa75c34490f5329a847c0"; V2EX_TAB="2|1:0|10:1440168432|8:V2EX_TAB|8:dGVjaA==|d85f10d93bbebf7d4a2940099b2d1e7619f79e42f4a195169b69026ba87a8cf6"; V2EX_LANG=zhcn' -H 'Origin: http://v2ex.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Referer: http://v2ex.com/signin' -H 'Connection: keep-alive' -H 'DNT: 1' --data 'u=mcxiaoke&p=password&once=87626&next=%2F' --compressed
'''

from __future__ import print_function
import requests
import random
from bs4 import BeautifulSoup as bs

login_url = 'http://v2ex.com/signin'
mission_url = 'https://www.v2ex.com/mission/daily'

headers = {
    'User-Agent': 'Mozilla/5.0 (Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44',
    'Referer': 'http://v2ex.com/signin',
}

payload = {
    'u': 'username',
    'p': 'password',
    'next': '/',
}

s = requests.Session()
r = s.get(login_url, headers=headers)
soup = bs(r.text, 'html.parser')
once = soup.find('input', {'name': 'once'})['value']
payload['once'] = once
r = s.post(login_url, payload, headers=headers)
# print(r.status_code)
# print(r.cookies)
r = s.get(mission_url, headers=headers)
soup = bs(r.text, 'html.parser')
once = soup.find(attrs={'class': 'super normal button'})['onclick']
print(once)
