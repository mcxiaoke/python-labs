#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 07:49:55

from fanfou import FanfouClient
import sys
#import dataset

# requests
# oauth2
# requests-oauthlib
#

if __name__ == '__main__':
    print sys.argv
    client = FanfouClient()
    #print client.login("test", "test")
    # print client.verify()
    #user = client.get_user("wangxing", mode="default", format="html")
    #timeline=client.get_user_timeline("blessedkristin", count=1)
    # print user
    # print timeline[0]


'''
{u'status': {u'favorited': False, u'truncated': False, u'text': u'\u5317\u4eac\u4e94\u73af\u5185\u4eba\u53e3\u636e\u8bf4\u662f1000\u4e07\u5de6\u53f3\uff0c\u4e94\u73af\u9762\u79ef\u63a5\u8fd1700\u5e73\u65b9\u516c\u91cc\uff0c\u5e73\u5747\u4e00\u5e73\u65b9\u516c\u91cc\u624d1.5\u4e07\u4eba\u3002', u'created_at': u'Wed Aug 05 12:59:18 +0000 2015', u'source': u'iPhone\u7248', u'in_reply_to_lastmsg_id': u'', u'in_reply_to_user_id': u'', u'in_reply_to_screen_name': u'', u'rawid': 185533910, u'id': u'C6bicoqOJu8'}, u'created_at': u'Sat May 12 14:24:26 +0000 2007', u'utc_offset': 28800, u'favourites_count': 114, u'screen_name': u'\u738b\u5174', u'friends_count': 731, u'url': u'', u'gender': u'\u7537', u'description': u'\u5982\u679c\u6211\u4e00\u6574\u5929\u90fd\u6ca1\u770b\u5230\u3001\u60f3\u5230\u3001\u6216\u505a\u8fc7\u4ec0\u4e48\u503c\u5f97\u5728\u996d\u5426\u4e0a\u8bf4\u7684\u4e8b\uff0c\u90a3\u8fd9\u4e00\u5929\u5c31\u592a\u6d51\u6d51\u5669\u5669\u4e86\u3002\r\n\r\n\u7f8e\u56e2\u521b\u59cb\u4eba\uff0c\r\n\u996d\u5426\u521b\u59cb\u4eba\uff0c\r\n\u6821\u5185\u7f51\u521b\u59cb\u4eba\uff0c\r\n\u975e\u5178\u578b\u6e05\u534e\u5de5\u79d1\u7537\u3002\r\n\r\nCreate like a god.\r\nCommand like a king.\r\nWork like a subordinate.', u'profile_image_url_large': u'http://avatar3.fanfou.com/l0/00/31/n3.jpg?1179311049', u'profile_image_url': u'http://avatar3.fanfou.com/s0/00/31/n3.jpg?1179311049', u'notifications': True, u'followers_count': 156346, u'birthday': u'0000-02-18', u'location': u'\u5317\u4eac \u6d77\u6dc0\u533a', u'following': True, u'statuses_count': 7684, u'protected': False, u'id': u'wangxing', u'name': u'\u738b\u5174'}
{u'user': {u'profile_image_url_large': u'http://avatar2.fanfou.com/l0/00/k5/g8.jpg?1290705252', u'id': u'blessedkristin', u'profile_sidebar_fill_color': u'#e2f2da', u'profile_text_color': u'#222222', u'followers_count': 282, u'profile_sidebar_border_color': u'#b2d1a3', u'location': u'\u5317\u4eac \u4e1c\u57ce\u533a', u'profile_background_color': u'#acdae5', u'utc_offset': 28800, u'statuses_count': 58715, u'description': u'\u53ea\u613f\u5e73\u5b89\u559c\u4e50\u5730\u6d3b\r\n\r\n\u611f\u8c22\u996d\u5426\u627f\u53d7\u4e86\u6211\u90a3\u4e48\u591a\u5b64\u5bc2\u6124\u6068\u4e0e\u72c2\u8e81\uff0c\u611f\u8c22\u996d\u5426\u8bb0\u5f55\u4e86\u6211\u751f\u547d\u4e2d\u4e5f\u8bb8\u53ea\u4f1a\u51fa\u73b0\u4e00\u6b21\u7684\u6216\u6e29\u60c5\u6216\u7f8e\u597d\u7684\u4e00\u70b9\u4e00\u6ef4\u3002\r\n\r\n\u4e0dfo\u4eba\uff0c\u4e0d\u8fc7fo\uff0c\u9664\u975e\u975e\u5e38\u5408\u62cd\u3002fo\u540e\u5f88\u5c11unfo\u3002\u7ecf\u5e38\u5220fo\u3002\r\n\r\n\u6ce8\uff1a\u4f1a\u65f6\u4e0d\u65f6\u6709\u4e1d\u5206\u88c2\u5206\u51fa\u4e00\u4e2a\u6a21\u8303\u5c0f\u6807\u5175\u9752\u86d9\u6765\u7763\u4fc3\u81ea\u5df1\u5b66\u4e60\u3002', u'friends_count': 161, u'profile_link_color': u'#0066cc', u'profile_image_url': u'http://avatar2.fanfou.com/s0/00/k5/g8.jpg?1290705252', u'notifications': False, u'birthday': u'1990-10-12', u'profile_background_image_url': u'http://avatar.fanfou.com/b0/00/k5/g8_1307173575.jpg', u'name': u'\u9752\u74e6\u7684\u65e7\u65f6\u5149', u'profile_background_tile': True, u'favourites_count': 1563, u'screen_name': u'\u9752\u74e6\u7684\u65e7\u65f6\u5149', u'url': u'http://blog.sina.com.cn/blessedkristin', u'gender': u'\u5973', u'created_at': u'Thu Nov 25 17:08:46 +0000 2010', u'protected': False, u'following': False}, u'favorited': False, u'truncated': False, u'text': u'\u5403\u5b8c\u996d\uff0c\u6d17\u7897\uff0c\u62d6\u5730\u6253\u626b\u536b\u751f\uff0c\u6d17\u6fa1\u6d17\u8863\u670d\u667e\u8863\u670d\uff0c\u4e0b\u697c\u5012\u5783\u573e\uff0c\u73b0\u5728\u8eba\u5728\u5e8a\u4e0a\u73a9\u624b\u673a\u5403\u54c8\u5bc6\u74dc\U0001f348\u6843\u5b50\U0001f351\u3002\u672c\u6765\u4ee5\u4e3a\u4f1a\u7ecf\u5e38\u51fa\u53bb\u73a9\uff0c\u628a\u676d\u5dde\u5927\u8857\u5c0f\u5df7\u90fd\u8d70\u904d\u7684\uff0c\u7ed3\u679c\u6839\u672c\u4e0d\u60f3\u52a8\u5f39\u3002\u539f\u6765\u751f\u6d3b\u8fd9\u4e48\u65e0\u804a\u554a\u3002 #\u5173\u4e8e\u676d\u5dde\u6211\u60f3\u7684\u90fd\u662f\u4f60#', u'created_at': u'Wed Aug 05 13:24:46 +0000 2015', u'source': u'\u624b\u673a\u4e0a\u7f51', u'in_reply_to_status_id': u'', u'in_reply_to_screen_name': u'', u'in_reply_to_user_id': u'', u'is_self': False, u'rawid': 185534790, u'id': u'KnB2bfapU7U', u'location': u'\u5317\u4eac \u4e1c\u57ce\u533a'}
'''

