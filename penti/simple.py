#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 08:35:05
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re

url_tpl = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei&page={0}'

urls = []
last=0

def myurl(a):
    return a.text and a.parent.name == 'li' and re.compile(u'\S+图卦\d{8}】.+').search(a.text)

for i in range(100):
    url = url_tpl.format(i)
    r = requests.get(url)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all(myurl)
    last=i
    if links:
        print('fetch page '+str(i))
        urls.extend(links)
    else:
        break

print(len(urls))
print(last)
