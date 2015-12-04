#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-12-04 16:38:11
from __future__ import print_function
import requests

OUTPUT = 'output'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.1234.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': '*/*',
            'Referer': 'http://music.163.com/'}

URL_TEMPLATE = 'http://music.163.com/api/mv/detail/?id=%s&type=mp4'



def get_mv_info(id):
    url = URL_TEMPLATE % id
    r = requests.get(url, headers=HEADERS)
    print(r.url)
    print(r.headers)
    print(r.json())

if __name__ == '__main__':
    get_mv_info('441097')


'''
sample data
curl 'http://music.163.com/api/mv/detail/?id=441097&type=mp4' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' -H 'Accept: */*' -H 'Referer: http://music.163.com/'  --compressed

{'Pragrma': 'no-cache', 'Content-Encoding': 'gzip', 'Transfer-Encoding': 'chunked', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT', 'Vary': 'Accept-Encoding', 'Server': 'nginx', 'Connection': 'keep-alive', 'Cache-Control': 'no-store, no-cache', 'Date': 'Fri, 04 Dec 2015 08:50:41 GMT', 'Content-Type': 'application/json;charset=UTF-8'}

{u'code': 200, u'subed': False, u'loadingPicFS': u'', u'bufferPicFS': u'', u'data': {u'commentThreadId': u'R_MV_5_441097', u'name': u'\ub5a8\ub824\uc694', u'brs': {u'480': u'http://v4.music.126.net/20151205165041/0fa4893df7752ea74a19eb590342ddf3/web/cloudmusic/ISAgMTAhMDAiNTIgIDUhIA==/mv/441097/8d811fe20eef5139adfff80ba91a40c5.mp4', u'240': u'http://v4.music.126.net/20151205165041/5fee12c81901fdedce7dc98447689b94/web/cloudmusic/ISAgMTAhMDAiNTIgIDUhIA==/mv/441097/275452c257c53b2e611d9b511a826a36.mp4', u'720': u'http://v4.music.126.net/20151205165041/9fe681aed9aff5cf1df37938af9eaace/web/cloudmusic/ISAgMTAhMDAiNTIgIDUhIA==/mv/441097/2a48a14e51a003562197609a0412a37a.mp4', u'1080': u'http://v4.music.126.net/20151205165041/1cca4e80e42efe3169f38a538fe5a3cb/web/cloudmusic/ISAgMTAhMDAiNTIgIDUhIA==/mv/441097/4d9e2312c476f96137eb557143ac9748.mp4'}, u'briefDesc': u'Stellar\u65b0\u5355MV19\u7981 \u6697\u793a\u6ee1\u6ee1\u5237\u6781\u9650', u'nType': 0, u'cover': u'http://p4.music.126.net/lTsYEnsxeV9eyKczTAB1QA==/7962663209711907.jpg', u'artistId': 127714, u'publishTime': u'2015-07-20', u'commentCount': 1129, u'artistName': u'Stellar', u'shareCount': 139, u'coverId': 7962663209711907, u'duration': 182000, u'playCount': 266988, u'subCount': 7608, u'id': 441097, u'desc': u''}, u'loadingPic': u'', u'bufferPic': u''}

'''
