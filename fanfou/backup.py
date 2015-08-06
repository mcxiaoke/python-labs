#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50

import fanfou
import cPickle as store
import utils
import time
from db import DB


def main():
    account = ("test", "test")
    saved_token = utils.load_oauth_token(account[0])
    print 'load saved token: %s for account: %s' % (saved_token, account[0])
    api = fanfou.FanfouClient()
    if saved_token:
        api.set_oauth_token(saved_token)
    if not api.is_verified():
        new_token = api.login(account[0], account[1])
        print 'save new token: %s' % new_token
        utils.save_oauth_token(account[0], new_token)
    user = api.get_user("androidsupport")
    print "prepare backup data for user: %s (%s)" % (
        user['screen_name'], user['id'])
    db = DB('%s_data.db' % user['id'])
    while(False):
        uid = user['id']
        count = 60
        top_status = db.get_top_status()
        max_id = top_status['sid'] if top_status else None
        print "top status: ", top_status
        print 'fetch timeline, max_id: %s' % max_id
        timeline = api.get_user_timeline(uid, count=count, max_id=max_id)
        if not timeline:
            break
        print len(timeline)
        c = db.bulk_insert_status(timeline)
        time.sleep(5)
        if len(timeline) < 60:
            break
    db.print_status()
    #print db.get_all_status_ids()


if __name__ == '__main__':
    main()
