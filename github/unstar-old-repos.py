#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-15 11:11:36
from __future__ import print_function, unicode_literals
import requests
import json
from config import ACCESS_TOKEN

STARS_URL = 'https://api.github.com/users/mcxiaoke/starred?direction=asc&sort=updated'  # GET
UNSTAR_URL = 'https://api.github.com/user/starred/{}'  # DELETE

HEADERS = {
    'Authorization': 'Bearer {}'.format(ACCESS_TOKEN)
}


while True:
    r = requests.get(STARS_URL)
    res = r.json()
    urls = [UNSTAR_URL.format(x['full_name']) for x in res]
    for url in urls:
        r1 = requests.delete(url, headers=HEADERS)
        print('DELETE {} Result:{}'.format(url, r1.status_code))
