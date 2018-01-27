#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 13:39:12
from __future__ import print_function
import requests
from bs4 import BeautifulSoup

r=requests.get('http://www.dapenti.com/blog/more.asp?name=xilei&id=102481')
r.encoding='gb2312'
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.find_all('img'))
