#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50

import fanfou
import utils
import time
import sys
from db import DB


def main(username,password,target=None):
    saved_token = utils.load_oauth_token(username)
    if saved_token:
        print 'load saved token: %s for %s' % (saved_token, username)
    else:
        print "no saved toen, get token from server..."
    api = fanfou.FanfouClient()
    if saved_token:
        api.set_oauth_token(saved_token)
    if not api.is_verified():
        new_token = api.login(username, password)
        print 'save new token: %s' % new_token
        utils.save_oauth_token(username, new_token)
    target_id= target if target else api.user['id']
    user = api.get_user(target_id)

    print "prepare backup data for user: %s (%s)" % (
        user['screen_name'], user['id'])
    db = DB('%s_data.db' % user['id'])
    # TODO 备份旧的中断后要能断点续传
    # TODO 如果有新增的也需要增量备份
    while(True):
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
        db.bulk_insert_status(timeline)
        time.sleep(5)
        if len(timeline) < 60:
            break
    db.print_status()
    #print db.get_all_status_ids()


if __name__ == '__main__':
    if len(sys.argv) <3:
        print "python usage %s username password target" % sys.argv[0]
        sys.exit(1)
    username=sys.argv[1]
    password=sys.argv[2]
    target=sys.argv[3] if len(sys.argv)>3 else None
    main(username,password,target)
