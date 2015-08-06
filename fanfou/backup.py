#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50

import fanfou
import utils
import time
import sys
from db import DB

DEFAULT_COUNT = 60


def fetch_newer_statuses(api, uid):
    # first ,check new statuses
    db = DB('%s_data.db' % uid)
    head_status = db.get_latest_status()
    if head_status:
        while(True):
            head_status = db.get_latest_status()
            since_id = head_status['sid'] if head_status else None
            print 'fetch timeline, since_id: %s' % since_id
            timeline = api.get_user_timeline(
                uid, count=DEFAULT_COUNT, since_id=since_id)
            if not timeline:
                break
            print len(timeline)
            db.bulk_insert_status(timeline)
            time.sleep(2)
            if len(timeline) < 60:
                break
    db.print_status()


def fetch_older_statuses(api, uid):
    # then, check older status
    db = DB('%s_data.db' % uid)
    while(True):
        tail_status = db.get_oldest_status()
        max_id = tail_status['sid'] if tail_status else None
        print 'fetch timeline, max_id: %s' % max_id
        timeline = api.get_user_timeline(
            uid, count=DEFAULT_COUNT, max_id=max_id)
        if not timeline:
            break
        print len(timeline)
        db.bulk_insert_status(timeline)
        time.sleep(2)
        if len(timeline) < 60:
            break
    db.print_status()


def main(username, password, target=None):
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
    target_id = target if target else api.user['id']
    user = api.get_user(target_id)
    uid = user['id']
    print "prepare backup data for user: %s (%s)" % (
        user['screen_name'], uid)
    #db = DB('%s_data.db' % uid)
    # first ,check new statuses
    fetch_newer_statuses(api, uid)
    # then, check older status
    fetch_older_statuses(api, uid)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "python usage %s username password target" % sys.argv[0]
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
    target = sys.argv[3] if len(sys.argv) > 3 else None
    main(username, password, target)
